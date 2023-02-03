import logging
import sys

from loguru import logger
from split_settings.tools import include, optional

include(
    "../common_components/base.py",
    "components/worker_apps.py",
    "../common_components/channels.py",
    "components/discord.py",
    "../common_components/django_extensions.py",
    optional("components/local_settings.py"),
)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=0)


logger.remove()
logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<red>Extra: {extra}</red> - <level>{message}</level>"
)

logger.add(sys.stdout,  colorize=True, format=logger_format, level="INFO")
