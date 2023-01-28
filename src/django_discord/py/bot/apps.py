from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.apps import AppConfig
from django.conf import settings


class DjangoDiscordPyBotAutoStartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_discord.py.bot"

    def ready(self):
        channel_layer = get_channel_layer()
        print("Sending start signal")

        logging_config = {
            config_key: getattr(settings, config_setting)
            for config_key, config_setting
            in [
                ("log_handler", 'DISCORD_BOT_LOG_HANDLER', ),
                ("log_formatter", 'DISCORD_BOT_LOG_FORMATTER', ),
                ("log_level", 'DISCORD_BOT_LOG_LEVEL', ),
                ("root_logger", 'DISCORD_BOT_ROOT_LOGGER', ),
            ]
            if hasattr(settings, config_setting)
        }
        async_to_sync(channel_layer.send)(
            "discord_bot",
            {
                "type": "start.discord.bot",
                "bot_path": settings.DISCORD_BOT_PATH,
                "reconnect": settings.DISCORD_BOT_RECONNECT,
                **logging_config,
            }
        )
        print("Start signal sent")
