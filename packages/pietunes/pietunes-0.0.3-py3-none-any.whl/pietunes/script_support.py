"""
PieTunes is an abstraction of Apple's Scripting Bridge API for iTunes.
Copyright (C) 2018  Brian Farrell

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

from textwrap import dedent


def _download(requested_playlist, requested_track):
    script = f"""
    tell application "iTunes"
        set playlist_target to some playlist ¬
            whose name is "{requested_playlist}"
        set len to count of tracks of playlist_target
        set target_collection to (tracks of playlist_target)
        repeat with i from 1 to number of items in target_collection
            set candidate to item i of target_collection
            if (name of candidate) = "{requested_track}" then
                download candidate
                exit repeat
            end if
        end repeat
    end tell
    """
    return dedent(script).encode('utf-8')


def _open_library(library_location):
    """launch iTunes with a given Library
    This script came from https://stackoverflow.com/a/1693973
    Courtesy of Nicholas Riley:
        https://stackoverflow.com/users/6372/nicholas-riley
    """

    script = f"""
    property altLibraryLocation : "{library_location}"
    property libraryLocationPref : ¬
        "com.apple.iTunes 'book:1:iTunes Library Location'"



    """
    return dedent(script).encode('utf-8')


def _quit_itunes():
    script = f"""
    tell application "System Events"
        if exists (application process "iTunes") then
            tell application "iTunes" to quit
        end if
    end tell
    """

    return dedent(script).encode('utf-8')
