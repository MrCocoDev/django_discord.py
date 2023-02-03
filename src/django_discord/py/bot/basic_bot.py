from typing import Any

import discord
from discord.ext import commands
from discord.ext.commands import Context
from django.conf import settings
from loguru import logger

description = """
A bot for friendly betting on league of legends
"""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=settings.DISCORD_PY_COMMAND_PREFEX, description=description, intents=intents)

log = logger


@bot.event
async def on_command_error(ctx: Context, error):
    log.bind(**{'ctx': ctx, 'error': error}).error("Discord bot had an error!")
    await ctx.send("Something went wrong!")


@bot.event
async def on_error(event_method: str, /, *args: Any, **kwargs: Any):
    log.bind(**{'event_method': event_method, 'args': args, 'kwargs': kwargs}).error("Discord bot had an error!")


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    logger.info("------")
