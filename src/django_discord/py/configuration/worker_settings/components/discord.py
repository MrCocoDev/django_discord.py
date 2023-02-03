import os

DISCORD_PY_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN', 'SET_THIS')
DISCORD_PY_COMMAND_PREFEX = "?"
DISCORD_BOT_PATH = 'django_discord.py.bot.basic_bot:bot'
DISCORD_BOT_RECONNECT = True
DISCORD_BOT_LOG_LEVEL = 'DEBUG'
DISCORD_BOT_PLUGINS = [
    'django_discord.py.example_bot.bot_plugins',
]
