import sys

from django_discord.py.cli import run_asgi_workers

if __name__ == "__main__":
    run_asgi_workers(*sys.argv[1:])
