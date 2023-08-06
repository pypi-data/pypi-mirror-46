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

This module should handle all of the command-line parsing and
invoke the correct command from commands.py
"""

import argparse

from mit.api import archive, show, six_degrees_of
from mit.__version__ import __version__


# create the top-level parser
parser = argparse.ArgumentParser(
    prog='mit',
    description='Use mit to manage iTunes',
    conflict_handler='resolve',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog='\n \n',
)

LIMIT_DEFAULT = 1000
parser.add_argument(
    '-l', '--limit',
    type=int,
    default=LIMIT_DEFAULT,
    help=(f'limit the number of operations performed by the command '
          f'to LIMIT\nDefaults to {LIMIT_DEFAULT}'
          f'\n \nExample:'
          f'\n\t\t`mit --limit 5 archive playlist Movies`'
          f'\n\t\twill archive up to 5 movies missing from the archive')
)

parser.add_argument(
    '-v',
    action='count',
    dest='verbosity',
)

parser.add_argument(
    '--version',
    action='version',
    version='%(prog)s ' + f'version { __version__}'
)

# Add subparser below for each mit command
subparsers = parser.add_subparsers(
    title='mit commands',
)


# create the parser for the "archive" command
parser_archive = subparsers.add_parser(
    'archive',
    help='archive help'
)

parser_archive.add_argument(
    'target',
    choices=[
        'playlist',
        'movie',
    ],
)

parser_archive.add_argument(
    'qualifier',
)

parser_archive.set_defaults(func=archive)


# create the parser for the "show" command
parser_show = subparsers.add_parser(
    'show',
    formatter_class=argparse.RawTextHelpFormatter,
    help='show help for show'
)

me_group = parser_show.add_mutually_exclusive_group()

parser_show.add_argument(
    'target',
    choices=[
        'playlist',
        'movie',
        'sources'
    ],
    metavar='target',
    help=('The type of iTunes object to show.'
          ' Choices include playlist, movie, or sources.')
)

parser_show.add_argument(
    'qualifier',
    nargs='?',
)

parser_show.add_argument(
    '-c', '--count',
    action='store_true',
    dest='count',
    help='Output the result set as a numbered list'
)

me_group.add_argument(
    '-d', '--delimited',
    action='store_true',
    dest='delimited',
    help=('Output the result in a delimited string for use in pipelines. '
          '\nThe Output for this option will omit any headers and footers'
          '\nThis option cannot be used with the [-t, --total] option')
)

parser_show.add_argument(
    '-j', '--json',
    action='store_true',
    dest='json',
    help='Output the extended result set in JSON'
)

me_group.add_argument(
    '-t', '--total',
    action='store_true',
    dest='total',
    help=('Include a total of the number of items in the output'
          '\nThis option cannot be used with the [-d, --delimited] option')
)

parser_show.add_argument(
    '-p', '--playlist',
    action='store',
    default=None,
    dest='playlist_arg',
    metavar='PLAYLIST',
    help=('When showing a movie or a song, etc., look for it in the '
          'PLAYLIST specifed')
)

parser_show.set_defaults(func=show)


# create the parser for the "archive" command
parser_six = subparsers.add_parser(
    'six',
    help='six degrees of separation help'
)

parser_six.add_argument(
    'target',
)

parser_six.add_argument(
    'qualifier',
)

parser_six.set_defaults(func=six_degrees_of)
