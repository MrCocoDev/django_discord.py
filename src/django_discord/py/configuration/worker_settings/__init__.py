from split_settings.tools import include, optional

include(
    "../common_components/base.py",
    "components/worker_apps.py",
    "../common_components/channels.py",
    "components/discord.py",
    optional("components/local_settings.py"),
)
