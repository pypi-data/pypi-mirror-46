# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Level implementations."""

from typing import Tuple, Tuple
from dataclasses import dataclass


@dataclass
class Level:
    """
    Associates a `name` (str) and a numeric `value` (int).
    You can construct a collection of `Level`s with the `from_names` factory method.

    >>> levels = Level.from_names(['DEBUG', 'INFO'])
    >>> levels
    (Level(name='DEBUG', value=0),
     Level(name='INFO', value=1))
    """

    name: str
    value: int

    def __lt__(self, other: 'Level') -> bool:
        """Compares `.value`."""
        return self.value < other.value

    def __ge__(self, other: 'Level') -> bool:
        """Compares `.value`."""
        return self.value >= other.value

    @classmethod
    def from_names(cls, names: Tuple[str]) -> Tuple['Level']:
        """Construct a set of Level objects."""
        return tuple(cls(name, value) for value, name in enumerate(names))


# sensible defaults
LEVELS   = Level.from_names(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
DEBUG    = LEVELS[0]
INFO     = LEVELS[1]
WARNING  = LEVELS[2]
ERROR    = LEVELS[3]
CRITICAL = LEVELS[4]