import asyncio
import logging
from typing import Optional, Union

import discord
from discord import Interaction, app_commands
from discord.ext.commands import Bot, Context
from django.dispatch import receiver

from django_discord.py.bot.signals import bot_error, bot_ready, command_error
from django_discord.py.plugins.datatypes import DjangoDiscordPlugin

plugin = DjangoDiscordPlugin()

log = logging.getLogger(__name__)


async def setup(bot: Bot):
    """
    This code runs as soon as the bot is available to your plugin, it won't necessarily
    be ready.
    """
    # Do not sync commands! You'll be rate limited.
    ...


@receiver(bot_ready, sender=Bot)
def my_handler(sender, bot: Bot, **kwargs):
    """
    Add your bot ready code here! But do not sync commands! You'll be rate limited.
    """
    ...


@receiver(command_error, sender=Bot)
def on_command_error(sender, bot: Bot, ctx: Context, error: Exception, **kwargs):
    """
    Add your bot error handling code here!
    """
    asyncio.ensure_future(ctx.send(f"Something went wrong! {error}"))


@receiver(bot_error, sender=Bot)
def on_error(sender, bot: Bot, event_method: str, event_args, event_kwargs, **kwargs):
    """
    Add your server error handling code here!
    """


@plugin.bot.command(description="Sync commands to servers")
async def sync(ctx: Context):
    plugin.bot.tree.copy_global_to(guild=discord.Object(id=ctx.guild.id))
    await plugin.bot.tree.sync(guild=discord.Object(id=ctx.guild.id))
    await ctx.send(
        "Syncing commands now!"
    )


@plugin.bot.tree.command(guilds=[discord.Object(id=802682445240991744)])
@app_commands.describe(number='Any number', string='Some random string')
async def guild_only(interaction: Interaction, number: int, string: str):
    await interaction.response.send_message(f'Modify {number=} {string=}', ephemeral=True)


@plugin.bot.tree.command()
@app_commands.describe(attachment='The file to upload')
async def global_command(interaction: discord.Interaction, attachment: discord.Attachment):
    await interaction.response.send_message(f'Thanks for uploading {attachment.filename}!', ephemeral=True)


@plugin.bot.command(description="Say 'Hello, world!'")
async def howdy(ctx: Context):
    log.info("Someone said 'Howdy', responding!")
    await ctx.send(
        f"Howdy, channel #{ctx.guild.id}! 🤠"
    )


class Permissions(app_commands.Group):
    """Manage permissions of a member."""

    def get_permissions_embed(self, permissions: discord.Permissions) -> discord.Embed:
        embed = discord.Embed(title='Permissions', colour=discord.Colour.blurple())
        permissions = [
            (name.replace('_', ' ').title(), value)
            for name, value in permissions
        ]

        allowed = [name for name, value in permissions if value]
        denied = [name for name, value in permissions if not value]

        embed.add_field(name='Granted', value='\n'.join(allowed), inline=True)
        embed.add_field(name='Denied', value='\n'.join(denied), inline=True)
        return embed

    @app_commands.command()
    @app_commands.describe(target='The member or role to get permissions of')
    async def get(self, interaction: discord.Interaction, target: Union[discord.Member, discord.Role]):
        """Get permissions for a member or role"""

        if isinstance(target, discord.Member):
            assert target.resolved_permissions is not None
            embed = self.get_permissions_embed(target.resolved_permissions)
            embed.set_author(name=target.display_name, url=target.display_avatar)
        else:
            embed = self.get_permissions_embed(target.permissions)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='in')
    @app_commands.describe(channel='The channel to get permissions in')
    @app_commands.describe(member='The member to get permissions of')
    async def _in(
            self,
            interaction: discord.Interaction,
            channel: Union[discord.TextChannel, discord.VoiceChannel],
            member: Optional[discord.Member] = None,
    ):
        """Get permissions for you or another member in a specific channel."""
        embed = self.get_permissions_embed(channel.permissions_for(member or interaction.user))
        await interaction.response.send_message(embed=embed)


# Another way to add commands
# To add the Group to your tree...
plugin.bot.tree.add_command(Permissions(), guild=discord.Object(id=802682445240991744))
