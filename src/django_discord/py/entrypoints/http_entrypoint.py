import sys

from django_discord.py.cli import run_daphne_server

if __name__ == "__main__":
    ip_address = '0.0.0.0'
    port = '8075'
    try:
        ip_address, port = sys.argv[1:]
    except ValueError:
        try:
            ip_address = sys.argv[1]
        except IndexError:
            # Use the default, probably a developer
            pass

    except Exception as e:
        print(f"We did not understand that, sorry! Here was the error: {e}")
        sys.exit(1)

    run_daphne_server(ip_address, port)
