from channels.db import database_sync_to_async
from discord.ext.commands import Context

from django_discord.py.bot import models


@database_sync_to_async
def save_discord_meta_models(ctx: Context):
    guild = models.DiscordGuild.objects.get_or_create(
        discord_id=ctx.guild.id,
    )

    channel = models.DiscordChannel.objects.get_or_create(
        discord_id=ctx.channel.id,
        discord_guild=guild,
    )

    user = models.DiscordUser.objects.get_or_create(
        name=ctx.author.name,
        discriminator=ctx.author.discriminator,
    )

    message = models.DiscordMessage.objects.get_or_create(
        discord_id=ctx.message.id,
        discord_guild=guild,
        discord_channel=channel,
        discord_user=user,
    )

    return guild, channel, user, message
