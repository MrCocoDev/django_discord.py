class BaseDjangoDiscordException(Exception):
    """
    Base exception for all intentional errors from this library
    """


class BotNotReadyYet(BaseDjangoDiscordException):
    """
    The bot isn't ready yet, someone used the library incorrectly?
    """


class MissingConfiguration(BaseDjangoDiscordException):
    """
    Something about the configuration is wrong, see the message for more details
    """
