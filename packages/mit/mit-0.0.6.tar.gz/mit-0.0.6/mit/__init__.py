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


    mit [args] [<command>] [<args>]

    mit show playlists --no-user  # Show a list of Playlists in iTunes - but
                                    only the ones that are defaults
                                    (no user created playlists)
"""
import sys

from mit.cli import parser

args_optional = set(
    {
        'limit': None,
        'verbosity': None,
    }
)


def main():
    args = parser.parse_args()
    args_given = set(vars(args))
    check = args_given ^ args_optional

    if len(check) > 0:
        args.func(args)
    else:
        parser.print_help()
        sys.exit()
