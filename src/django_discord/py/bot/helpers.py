
from functools import singledispatch

from channels.db import database_sync_to_async
from discord import Interaction
from discord.ext.commands import Context
from loguru import logger

from django_discord.py.bot import models

log = logger


@singledispatch
def save_discord_meta_models(obj):
    raise NotImplementedError


@save_discord_meta_models.register
@database_sync_to_async
def _(obj: Context):
    log.debug("Creating discord guild from context")
    guild, _ = models.DiscordGuild.objects.get_or_create(
        discord_id=obj.guild.id,
    )

    log.debug("Creating discord channel from context")
    channel, _ = models.DiscordChannel.objects.get_or_create(
        discord_id=obj.channel.id,
        discord_guild=guild,
    )

    log.debug("Creating discord user from context")
    user, _ = models.DiscordUser.objects.get_or_create(
        name=obj.author.name,
        discriminator=obj.author.discriminator,
    )

    log.debug("Creating discord message from context")
    message, _ = models.DiscordMessage.objects.get_or_create(
        discord_id=obj.message.id,
        discord_guild=guild,
        discord_channel=channel,
        discord_user=user,
    )

    return guild, channel, user, message


@save_discord_meta_models.register
@database_sync_to_async
def _(obj: Interaction):
    log.debug("Creating discord guild from interaction")
    guild, _ = models.DiscordGuild.objects.get_or_create(
        discord_id=obj.guild.id,
    )

    log.debug("Creating discord channel from interaction")
    channel, _ = models.DiscordChannel.objects.get_or_create(
        discord_id=obj.channel.id,
        discord_guild=guild,
    )

    log.debug("Creating discord user from interaction")
    user, _ = models.DiscordUser.objects.get_or_create(
        name=obj.user.name,
        discriminator=obj.user.discriminator,
    )

    log.debug("Creating discord message from interaction")
    if obj.message and obj.message.id:
        message, _ = models.DiscordMessage.objects.get_or_create(
            discord_id=obj.message.id,
            discord_guild=guild,
            discord_channel=channel,
            discord_user=user,
        )
    else:
        message = None

    return guild, channel, user, message
