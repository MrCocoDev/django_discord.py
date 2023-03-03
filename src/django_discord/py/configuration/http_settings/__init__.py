import os

from split_settings.tools import include, optional

include(
    "../common_components/base.py",
    "../common_components/channels.py",
    "../common_components/django_extensions.py",
    optional(
        os.getenv(
            "DJANGO_DISCORD_PY_SERVER_LOCAL_SETTINGS",
            "components/local_settings.py",
        ),
    ),
)
