"""
MIT is a Python utility to Manage iTunes from the command line.
Copyright (C) 2019  Brian Farrell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact: brian.farrell@me.com
"""

import sys
from textwrap import TextWrapper

from mit import show as showit

__all__ = ['archive', 'show', 'six_degrees_of']

DEFAULT_INDENT = 3


def archive(args):
    pass


def show(args):
    try:
        target = args.target
        qualifier = args.qualifier
        if target == 'playlist':
            value = showit._show_playlist(qualifier, args)
        elif target == 'movie':
            value = showit._show_movie(qualifier, args)
        elif target == 'sources':
            value = showit._show_sources(args)
        return value
    except Exception as e:
        wrapper = TextWrapper(
            width=showit.OUTPUT_WIDTH,
            tabsize=showit.TAB_SIZE,
        )
        err = wrapper.fill(f'{e}')
        print(f'\n{err}\n')
        sys.exit(1)


def six_degrees_of(target='Kevin Bacon'):
    pass
