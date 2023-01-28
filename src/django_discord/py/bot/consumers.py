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
    running: bool = False
    bot_task: asyncio.Task = None

    def start_discord_bot(self, event):
        if self.running:
            return

        bot_path = event['bot_path']
        reconnect: bool = event['reconnect']
        log_handler: Optional[logging.Handler] = event.get('log_handler', MISSING)
        log_formatter: logging.Formatter = event.get('log_formatter', MISSING)
        log_level: int = event.get('log_level', MISSING)
        root_logger: bool = event.get('root_logger', False)

        bot: Bot = import_by_path(bot_path)
        bot_token: str = settings.DISCORD_PY_BOT_TOKEN

        async def runner():
            async with bot:
                await bot.start(bot_token, reconnect=reconnect)

        if log_handler is not None:
            utils.setup_logging(
                handler=log_handler,
                formatter=log_formatter,
                level=log_level,
                root=root_logger,
            )

        self.bot_task = asyncio.create_task(runner())

    def is_bot_running(self):
        return not self.bot_task.done() and not self.bot_task.cancelled()
