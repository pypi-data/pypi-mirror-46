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

from pietunes.api import App, NotFoundError

app = App()


def _get_all_playlists():
    return app.playlists


def _get_playlist(name):
    try:
        return app.get_playlist(name)
    except NotFoundError as e:
        print(e)
        sys.exit(1)


def _get_movie(collection, title):
    try:
        return app.get_track(collection, title)
    except NotFoundError as e:
        print(e)
        sys.exit(1)


def _get_tracks(playlist):
    try:
        return app.get_tracks(playlist)
    except NotFoundError as e:
        print(e)
        sys.exit(1)


def _get_sources():
    return app.get_sources()


class InputError(Exception):
    """
    Input Error
    This error is thrown when there is an invalid command line option present.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
