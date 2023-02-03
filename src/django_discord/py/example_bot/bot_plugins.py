import logging

from discord.ext.commands import Context

from django_discord.py.plugins.datatypes import DjangoDiscordPlugin

plugin = DjangoDiscordPlugin()

log = logging.getLogger(__name__)


@plugin.command(description="Say 'Hello, world!'")
async def howdy(ctx: Context):
    log.info("Someone said 'Howdy', responding!")
    await ctx.send(
        f"Howdy, channel #{ctx.channel.id}! 🤠"
    )
