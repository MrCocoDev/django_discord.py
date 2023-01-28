"""
ASGI config for django_discord.py project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import importlib
import os

from channels.routing import ChannelNameRouter, ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_discord.py.configuration.http_settings")

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.

django_asgi_app = get_asgi_application()

# Import after django is setup so we can count on settings being initialized
consumers_module = importlib.import_module('django_discord.py.bot.consumers')

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "channel": ChannelNameRouter(
            {
                "discord_bot": consumers_module.BaseDiscordConsumer.as_asgi(),
            }
        ),
    }
)
