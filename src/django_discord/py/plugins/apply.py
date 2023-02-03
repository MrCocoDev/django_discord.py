from discord.ext.commands import Bot

from django_discord.py.plugins.datatypes import CommandDefinition, DjangoDiscordPlugin


def apply_plugin(bot: Bot, plugin: DjangoDiscordPlugin):
    command: CommandDefinition
    for command in plugin.command_definitions:
        bot.command(*command.args, **command.kwargs)(command.callable)
