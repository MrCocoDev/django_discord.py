import os

from daphne.cli import CommandLineInterface
from django.core.management import execute_from_command_line


def run_daphne_server(ip_address, ip_port):
    CommandLineInterface().run(
        (
            'django_discord.py.configuration.asgi:application',
            '--bind',
            ip_address,
            '--port',
            ip_port,
        )
    )


def run_asgi_workers(*channels):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_discord.py.configuration.worker_settings")

    if not channels:
        channels = ('discord_bot', )

    execute_from_command_line(('manage.py', 'runworker', *channels))
