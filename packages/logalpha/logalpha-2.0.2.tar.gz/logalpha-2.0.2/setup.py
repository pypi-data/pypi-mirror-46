# This file is part of the LogAlpha package.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Build and installation script for LogAlpha."""

# standard libs
import os
from setuptools import setup, find_packages

# internal libs
from logalpha.__meta__ import (__appname__,
                               __version__,
                               __authors__,
                               __contact__,
                               __license__,
                               __description__)


def readme_file():
    """Use README.md as long_description."""
    with open(os.path.join(os.path.dirname(__file__), "README.md"), 'r') as readme:
        return readme.read()


setup(
    name             = __appname__,
    version          = __version__,
    author           = __authors__,
    author_email     = __contact__,
    description      = __description__,
    license          = __license__,
    keywords         = 'python minimalist logging package',
    url              = 'https://logalpha.readthedocs.io',
    packages         = find_packages(),
    long_description = readme_file(),
    classifiers      = ['Development Status :: 5 - Production/Stable',
                        'Topic :: System :: Logging',
                        'Programming Language :: Python :: 3.7',
                        'License :: OSI Approved :: Apache Software License', ],
    entry_points     = {'console_scripts': []},
)
