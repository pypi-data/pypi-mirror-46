# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""ANSI color definitions and management."""

from typing import Tuple
from dataclasses import dataclass, field


NAMES = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

ANSI_RESET = '\033[0m'
ANSI_COLORS = {prefix: {color: '\033[{prefix}{num}m'.format(prefix=i + 3, num=j) for j, color in enumerate(NAMES)}
               for i, prefix in enumerate(['foreground', 'background'])}


@dataclass
class Color:
    """
    Associates a `name` (str) with its corresponding `foreground` and `background` (str) 
    ANSI codes. You can construct one or more instances using the factory methods.

    from_name(name: str) -> Color:
        Returns a Color by looking up its codes in the ANSI_COLORS dictionary.

    from_names(names: Tuple[names]) -> Tuple[Color]:
        Returns a tuple of Color instances using the singular `from_name` factory.
    
    Example:
    >>> colors = Color.from_names(['blue', 'green'])
    >>> colors
    (Color(name='blue', foreground='\x1b[34m', background='\x1b[44m'),
     Color(name='green', foreground='\x1b[32m', background='\x1b[42m'))
    """

    name: str
    foreground: str
    background: str

    # the ANSI reset code is an attribute but not a variable
    reset: str = field(default=ANSI_RESET, init=False, repr=False)

    @classmethod
    def from_name(cls, name: str) -> 'Color':
        """Lookup ANSI code by `name`."""
        return cls(name, ANSI_COLORS['foreground'][name], ANSI_COLORS['background'][name])

    @classmethod
    def from_names(cls, names: Tuple[str]) -> Tuple['Color']:
        """Create collection of colors by `name`."""
        return tuple(cls.from_name(name) for name in names)


COLORS  = Color.from_names(NAMES)
BLACK   = COLORS[0]
RED     = COLORS[1]
GREEN   = COLORS[2]
YELLOW  = COLORS[3]
BLUE    = COLORS[4]
MAGENTA = COLORS[5]
CYAN    = COLORS[6]
WHITE   = COLORS[7]
