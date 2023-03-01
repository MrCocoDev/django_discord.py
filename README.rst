.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/django-discord-py.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/django-discord-py
    .. image:: https://readthedocs.org/projects/django-discord-py/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://django-discord-py.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/django-discord-py/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/django-discord-py
    .. image:: https://img.shields.io/pypi/v/django-discord-py.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/django-discord-py/
    .. image:: https://img.shields.io/conda/vn/conda-forge/django-discord-py.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/django-discord-py
    .. image:: https://pepy.tech/badge/django-discord-py/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/django-discord-py
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/django-discord-py

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=================
django-discord-py
=================


    An easy-to-use, easy-to-start with Discord.py bot with Django built right in.


Discord bots are really cool, and Django provides a lot of functionality for free. For a lot of developers
this project may be too heavy weight to make sense. However, if you're used to Django and want to start
writing Discord bots then this should be a great place for you to start.


Important Notes Before We Get Started
=====================================

If you're new to developing django or have never installed a django server as a package before
you may be used to running `python manage.py <command>`. For this project you will instead run

::

  django-discord.py <command>

If you don't want this you can also install this package as normal and import the parts you want
to use in your django project.


Prerequisites
=============

By default this project requires Redis. Find installation instructions for you system at their site: https://redis.com


Installation
============

We recommend installing from PIP

::

  pip install --upgrade django_discord_py

If you want to install from source

::

  git clone <this_repo>
  cd <this_repo>
  pip install -e "."


Basic Bot Usage
===============

Using the console_scripts entrypoint

::

  python3 -m venv your_venv
  source your_venv/bin/activate
  pip install --upgrade django_discord_py
  discord-bot

Using the module directly

::

  python3 -m venv your_venv
  source your_venv/bin/activate
  pip install --upgrade django_discord_py
  python -m django_discord.py.entrypoints.channels_entrypoint


Basic Django Server Usage
=========================

Using the console_scripts entrypoint

::

  python3 -m venv your_venv
  source your_venv/bin/activate
  pip install --upgrade django_discord_py
  django-server

Using the module directly

::

  python3 -m venv your_venv
  source your_venv/bin/activate
  pip install --upgrade django_discord_py
  python -m django_discord.py.entrypoints.http_entrypoint


.. _pyscaffold-notes:


More Advanced Usage
===================

::

    export DJANGO_SETTINGS_MODULE='path.to.your.settings'

    # path.to.your.settings.py
    from from django_discord.py.configuration.common_components.base import INSTALLED_APPS
    DISCORD_BOT_PATH = 'path.to.your.discord.bot.definition'
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        'your_django_app',
    ]

Doing this will allow you to fully configure the Django application. You can also
set up a django project normally and do:

::

    # path.to.your.settings.py
    DISCORD_BOT_PATH = 'path.to.your.discord.bot.definition'
    INSTALLED_APPS = [
        ...,
        'django_discord.py.bot',
        ...,
    ]

But you will be responsible for starting the `channels` workers yourself.


Sending Your First Discord Bot Message
======================================

Add the bot to your discord server. Then launch the bot process using the instructinos above.
In a separate shell run

::

    # sh
    python -m django_discord.py shell_plus

This will launch an `IPython` shell with Django initialized.

In your discord server say "Hi!" to the bot:

::

    # discord
    ?hi

The bot will respond with the channel ID for the current channel. Copy the ID without the `#` and
run the following in your `IPython` shell:

::

    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    await channel_layer.send('discord_bot', {'type': 'send.message', 'channel': COPY_FROM_DISCORD, 'content': 'This is cool!'})


Extending The Server For Your Own Needs
=======================================

Obviously, you will want your bot to do more than just respond to `?hi`. To extend this bot
you can set **DJANGO_SETTINGS_MODULE** in your environment to your own settings file. From
there you will have all the normal controls over Django that you're used to.

For ease-of-use you can see **.env.example** for a list of import environment variables.


Using the plugin system
=======================

You can add your commands to the discord bot via plugins! To do this set:

::

   # settings.py

   DISCORD_BOT_PLUGINS = [
      'django_discord.py.example_bot.bot_plugins',
   ]

Plugin files are loaded _after_ django settings so it is safe to access the database at the module
level. A basic plugin might look like this:

::

   from discord.ext.commands import Context
   from django_discord.py.plugins.datatypes import DjangoDiscordPlugin

   plugin = DjangoDiscordPlugin()

   @plugin.bot.command(description="Say 'Hello, world!'")
   async def howdy(ctx: Context):
       await ctx.send(
           f"Howdy, channel #{ctx.channel.id}! 🤠"
       )

See the example plugin for more hooks and tips:

::

   django_discord.py.example_bot.bot_plugins


Making Changes & Contributing
=============================

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    pip install pre-commit
    cd django-discord-py
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

Don't forget to tell your contributors to also install and use pre-commit.

.. _pre-commit: https://pre-commit.com/


Note
====

This project has been set up using PyScaffold 4.3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
