import dataclasses
from typing import Callable


class DjangoDiscordPlugin:
    command_definitions = []

    def command(self, function=None, /, *args, **kwargs):
        def decorator(func):
            self.command_definitions.append(
                CommandDefinition(
                    callable=func,
                    args=args,
                    kwargs=kwargs,
                )
            )

        if function:
            return decorator(function)
        else:
            return decorator


@dataclasses.dataclass
class CommandDefinition:
    callable: Callable
    args: tuple
    kwargs: dict
