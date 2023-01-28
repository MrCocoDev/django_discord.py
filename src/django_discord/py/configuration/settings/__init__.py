from split_settings.tools import include, optional

include(
    "components/base.py",
    "components/channels.py",
    "components/discord.py",
    optional("components/local_settings.py"),
)
