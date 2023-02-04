from typing import ClassVar

from django_discord.py.exceptions import BotNotReadyYet


class DjangoDiscordPlugin:
    command_definitions = []

    bot_proxy: ClassVar

    @property
    def bot(self):
        the_bot = type(self).bot_proxy
        if not the_bot:
            raise BotNotReadyYet("The bot isn't ready yet! Have you started the bot?")
        return the_bot
