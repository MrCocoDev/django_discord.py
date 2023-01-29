import asyncio
import logging
from typing import Optional

from channels.consumer import AsyncConsumer
from daphne.utils import import_by_path
from discord import utils
from discord.ext.commands import Bot
from discord.utils import MISSING
from django.conf import settings


class BaseDiscordConsumer(AsyncConsumer):
    bot_task: asyncio.Task = None
    bot: Bot = None

    async def start_discord_bot(self, event):
        print("Received start signal")
        if await self.is_bot_running():
            print("Bot is already running, doing nothing")
            return

        print("Unpacking signal for bot parameters")
        bot_path = event['bot_path']
        reconnect: bool = event['reconnect']

        log_handler: Optional[logging.Handler] = event.get('log_handler', MISSING)
        log_formatter: logging.Formatter = event.get('log_formatter', MISSING)
        log_level: int = event.get('log_level', MISSING)
        root_logger: bool = event.get('root_logger', False)

        print(f"Importing '{bot_path}' ...")
        self.bot: Bot = import_by_path(bot_path)

        print("Grabbing bot auth token from settings")
        bot_token: str = settings.DISCORD_PY_BOT_TOKEN

        async def runner(bot, token, reconnect):
            async with bot:
                await bot.start(token, reconnect=reconnect)

        if log_handler is not None:
            utils.setup_logging(
                handler=log_handler,
                formatter=log_formatter,
                level=log_level,
                root=root_logger,
            )

        print("Creating bot loop")
        bot_coro = runner(self.bot, bot_token, reconnect)
        print("Running bot")
        self.bot_task = asyncio.create_task(bot_coro)

    async def is_bot_running(self):
        if not self.bot_task:
            return False

        return not self.bot_task.done() and not self.bot_task.cancelled()

    async def send_message(self, event: dict):
        if not self.is_bot_running():
            raise ValueError("Bot is not running!")
        event.pop('type')
        channel: int = event.pop('channel')
        content: str = event.pop('content', None)

        await self.bot.get_channel(channel).send(
            content=content,
            **event,
        )
