from typing import Any

import discord
from discord.ext import commands
from discord.ext.commands import Context
from django.conf import settings
from loguru import logger

from django_discord.py.bot.signals import bot_error, bot_ready, command_error

description = settings.DISCORD_BOT_DESCRIPTION

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=settings.DISCORD_PY_COMMAND_PREFEX, description=description, intents=intents)

log = logger


@bot.event
async def on_command_error(ctx: Context, error):
    log.bind(**{'ctx': ctx, 'error': error}).error("Discord bot had an error!")
    command_error.send_robust(sender=bot.__class__, ctx=ctx, error=error)
    if not command_error.receivers:
        await ctx.send("Something went wrong! Add a listener to command_error to replace this message!")


@bot.event
async def on_error(event_method: str, /, *args: Any, **kwargs: Any):
    log.bind(**{'event_method': event_method, 'args': args, 'kwargs': kwargs}).error("Discord bot had an error!")
    bot_error.send_robust(sender=bot.__class__, event_method=event_method, event_args=args, event_kwargs=kwargs)


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    logger.info("------")
    bot_ready.send_robust(sender=bot.__class__, bot=bot)
