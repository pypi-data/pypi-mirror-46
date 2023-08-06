# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Handler implementations."""

import io
import sys
from dataclasses import dataclass
from multiprocessing import Queue
from typing import Any

from .levels import Level
from .messages import Message


@dataclass
class Handler:
    """
    Core message handling interface.
    A Handler associates a logging level with a resource.
    """

    level: Level
    resource: Any

    def write(self, message: Message) -> None:
        """Publish `message` to `resource` after calling `format`."""
        print(self.format(message), file=self.resource, flush=True)

    def format(self, message: Message) -> Any:
        """Format `message` into necessary output.`"""
        return message.content


@dataclass
class FileHandler(Handler):
    """A `Handler` whose resource is file-like."""

    level: Level
    resource: io.TextIOWrapper

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the file `resource`. Arguments passed to open(...)."""
        self.resource = open(*args, **kwargs)
    
    def __enter__(self) -> 'FileHandler':
        return self
    
    def __exit__(self, *exc) -> None:
        """Releases the file `resource`."""
        self.resource.close()
    
    def __del__(self) -> None:
        """Releases the file `resource`."""
        self.resource.close()


@dataclass
class ConsoleHandler(FileHandler):
    """A `Handler` whose resource is `sys.stderr`."""

    level: Level
    resource: io.TextIOWrapper = sys.stderr


@dataclass
class QueueHandler(Handler):
    """Calls `.put` on the member queue `resource`."""

    level: Level
    resource: Queue

    def write(self, message: Message) -> None:
        self.resource.put(message)
