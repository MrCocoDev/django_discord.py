import asyncio
import logging
from importlib import import_module
from typing import Optional

from channels.consumer import AsyncConsumer
from daphne.utils import import_by_path
from discord import utils
from discord.ext.commands import Bot
from discord.utils import MISSING
from django.conf import settings
from loguru import logger

from django_discord.py.plugins.apply import apply_plugin


class BaseDiscordConsumer(AsyncConsumer):
    bot_task: asyncio.Task = None
    bot: Bot = None

    async def start_discord_bot(self, event):
        logger.info("Received start signal")
        if await self.is_bot_running():
            logger.info("Bot is already running, doing nothing")
            return

        logger.info("Unpacking signal for bot parameters")
        bot_path = event['bot_path']
        reconnect: bool = event['reconnect']

        log_handler: Optional[logging.Handler] = event.get('log_handler', MISSING)
        log_formatter: logging.Formatter = event.get('log_formatter', MISSING)
        log_level: int = event.get('log_level', MISSING)
        root_logger: bool = event.get('root_logger', False)

        logger.info(f"Importing '{bot_path}' ...")
        self.bot: Bot = import_by_path(bot_path)

        logger.info("Grabbing bot auth token from settings")
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
        logger.info("Loading plugins")
        plugin_paths = event.get('plugins', [])
        for plugin_path in plugin_paths:
            module = import_module(plugin_path)
            plugin = getattr(module, 'plugin')
            if not plugin:
                logger.error("Improperly configured plugin module found %s. Where is the `plugin` attribute?", module)
                continue
            apply_plugin(self.bot, plugin)

        logger.info("Creating bot loop")
        bot_coro = runner(self.bot, bot_token, reconnect)

        logger.info("Running bot")
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
