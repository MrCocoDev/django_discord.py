import logging

import discord
from discord.ext import commands
from django.conf import settings

description = """
A bot for friendly betting on league of legends
"""

intents = discord.Intents.default()

bot = commands.Bot(command_prefix=settings.DISCORD_PY_COMMAND_PREFEX, description=description, intents=intents)

log = logging.getLogger(__name__)


@bot.event
async def on_command_error(ctx, error):
    log.error("Discord bot had an error!", extra={'data': {'ctx': ctx, 'error': error}})
