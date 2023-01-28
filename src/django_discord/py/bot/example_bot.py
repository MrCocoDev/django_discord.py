import logging
from typing import Any

import discord
from discord.ext import commands
from discord.ext.commands import Context
from django.conf import settings

description = """
A bot for friendly betting on league of legends
"""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=settings.DISCORD_PY_COMMAND_PREFEX, description=description, intents=intents)

log = logging.getLogger(__name__)


@bot.event
async def on_command_error(ctx: Context, error):
    log.error("Discord bot had an error!", extra={'data': {'ctx': ctx, 'error': error}})
    await ctx.send("Something went wrong!")


@bot.event
async def on_error(event_method: str, /, *args: Any, **kwargs: Any):
    log.error("Discord bot had an error!", extra={'data': {'event_method': event_method, 'args': args, 'kwargs': kwargs}})


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command(description="Say 'Hello, world!'")
async def hi(ctx: Context):
    print("Someone said 'Hi', responding!")
    await ctx.send(
        "Hello, world!"
    )
