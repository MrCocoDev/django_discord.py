from django_discord.py.configuration.common_components.base import INSTALLED_APPS

INSTALLED_APPS = [
    *INSTALLED_APPS,
    "django_discord.py.bot",
]
