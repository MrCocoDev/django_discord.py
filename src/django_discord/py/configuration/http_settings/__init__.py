from split_settings.tools import include, optional

include(
    "../common_components/base.py",
    "../common_components/channels.py",
    optional("components/local_settings.py"),
)
