# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.


"""Logger implementations."""

# standard libs
import functools
from typing import Any, Tuple, List, Dict, Callable

# internal libs
from .levels import Level, LEVELS
from .colors import Color, BLUE, GREEN, YELLOW, RED, MAGENTA
from .handlers import Handler
from .messages import Message


# dictionary of parameter-less functions
CallbackMethod = Callable[[], Any]


class Logger:
    """
    Core logging interface.
    """

    # default configuration
    levels: Tuple[Level] = LEVELS
    colors: Tuple[Color] = (BLUE, GREEN, YELLOW, RED, MAGENTA)
    handlers: List[Handler] = list()

    callbacks: Dict[str, CallbackMethod] = dict()

    # redefine to construct with callbacks
    Message: type = Message

    def __init__(self) -> None:
        """Setup instance; define level methods."""
        self._setup_level_methods()

    def write(self, level: Level, content: Any) -> None:
        """Publish `message` to all `handlers`."""

        message = self.Message(level=level, content=content,
                               **self.evaluate_callbacks())

        for handler in self.handlers:
            if message.level >= handler.level:
                handler.write(message)

    def __call__(self, *args, **kwargs) -> None:
        """Short-hand method for `Logger.write`."""
        self.write(*args, **kwargs)

    def evaluate_callbacks(self) -> Dict[str, Any]:
        """Evaluates all methods in `callbacks` dictionary."""
        return dict(zip(self.callbacks.keys(),
                        map(lambda method: method(),
                            self.callbacks.values())))

    def _setup_level_methods(self) -> None:
        """Create member functions for all levels."""
        for level in self.levels:
            method = functools.partial(self.write, level)
            method.__doc__ = (f'Alias to {self.__class__.__name__}.write('
                              f'level={level}, content=...)')
            setattr(self, level.name.lower(), method)

