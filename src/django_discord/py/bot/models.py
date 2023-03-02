from django.db import models


def meta_fields():
    return models.DateTimeField(auto_now_add=True), models.DateTimeField(auto_now=True)


class DiscordGuild(models.Model):
    created, updated = meta_fields()

    discord_id = models.IntegerField()


class DiscordChannel(models.Model):
    created, updated = meta_fields()

    discord_id = models.IntegerField()
    discord_guild = models.ForeignKey(to=DiscordGuild, on_delete=models.CASCADE, null=True)


class DiscordUser(models.Model):
    created, updated = meta_fields()

    name = models.CharField(max_length=256)
    discriminator = models.CharField(max_length=256)


class DiscordMessage(models.Model):
    created, updated = meta_fields()

    discord_id = models.IntegerField()
    discord_guild = models.ForeignKey(to=DiscordGuild, on_delete=models.CASCADE, null=True)
    discord_channel = models.ForeignKey(to=DiscordChannel, on_delete=models.CASCADE, null=True)
    discord_user = models.ForeignKey(to=DiscordUser, on_delete=models.CASCADE, null=True)
