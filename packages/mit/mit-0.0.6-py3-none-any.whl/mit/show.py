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

import re
from textwrap import TextWrapper

from mit import core

OUTPUT_WIDTH = 120
ITEM_KEY_WIDTH = 20
NUMBER_PREFIX_SIZE = 7
TAB_SIZE = 4
DEFAULT_INDENT = (TAB_SIZE ^ 3)


def _show_playlist(qualifier, args):
    if qualifier == 'all':
        if args.playlist_arg:
            err = ('The qualifier \'all\' can not be used in '
                   'conjunction with a custom playlist speciified by the '
                   '\'-p/--playlist\' option.')
            raise core.InputError(err)
        header = f'iTunes Playlists'
        playlist = core._get_all_playlists()
        _show_result(header, playlist, args)
    else:
        playlist = core._get_playlist(qualifier)
        header = f'Playlist: {playlist.name()}'
        tracks = core._get_tracks(playlist)
        _show_result(header, tracks, args)


def _show_movie(qualifier, args):
    p = args.playlist_arg if args.playlist_arg else 'Movies'
    playlist = core._get_playlist(p)

    if qualifier == 'downloads':
        _get_downloaded_files(playlist)
    else:
        movies = core._get_tracks(playlist)
        movie = core._get_movie(movies, qualifier)
        header = f'\n{movie.name()}'
        data = dict(movie.properties())
        _show_result(header, data, args)


def _show_sources(args):
    header = 'iTunes Sources'
    data = core._get_sources()
    _show_result(header, data, args)


def _show_result(header, data, args):
    if args.json:
        _output_json(header, data, args)
    elif args.delimited:
        _output_delimited(header, data, args)
    else:
        _output_table(header, data, args)


def _output_table(header, data, args):
    global DEFAULT_INDENT
    if args.count:
        DEFAULT_INDENT += NUMBER_PREFIX_SIZE

    if type(data) == dict:
        DEFAULT_INDENT += ITEM_KEY_WIDTH + 2
        record_enum = enumerate(sorted(data.items()), start=1)
        format_record = _format_kv
    else:
        record_enum = enumerate(iter(data), start=1)
        format_record = _format_string

    # HEADER
    _print_header(header)

    # BODY
    for i, item in record_enum:
        if i <= args.limit:
            count_string = _get_count_string(i, args)
            item_string = format_record(item)
            item_string = count_string + item_string
            _print_record(item_string)
        else:
            i -= 1
            break

    # FOOTER
    _print_footer(i, args)


def _print_header(header):
    header = '\n' + header
    header += f'\n{"=" * OUTPUT_WIDTH}\n'
    print(header)


def _print_record(item_string):
    wrapper = TextWrapper(
        width=OUTPUT_WIDTH,
        tabsize=TAB_SIZE,
        subsequent_indent=' ' * DEFAULT_INDENT
    )
    record = wrapper.fill(f'\t{item_string}')
    print(record)


def _print_footer(i, args):
    # FOOTER
    if args.total:
        footer = f'\n{"-" * OUTPUT_WIDTH}'
        footer += f'\nTotal: {i}'
        print(footer)
    print('\n')


def _format_kv(item):
        k, v = item
        words = re.sub('(?!^)([A-Z][a-z]+|ID)', r' \1', k).split()
        k = ' '.join([word.capitalize() for word in words])
        try:
            item_string = f'{k.descriptorType:>{ITEM_KEY_WIDTH}}:\t{v}'
        except AttributeError as e:
            item_string = f'{k:>{ITEM_KEY_WIDTH}}:\t{v}'

        return item_string


def _format_string(item):
    item_string = f'{item.name()}'

    return item_string


def _get_count_string(i, args):
    if args.count:
        count_string = (f'{i:>{NUMBER_PREFIX_SIZE}}.  ')
    else:
        count_string = ''

    return count_string


def _output_json(header, data, args):
    pass


def _output_delimited(header, data, args):
    pass


def _fuzzy_match(target, unknown):
    pass


def _get_downloaded_files(playlist):
    for t in playlist.fileTracks():
        print(f'{t.location()}')
    print('\n')
