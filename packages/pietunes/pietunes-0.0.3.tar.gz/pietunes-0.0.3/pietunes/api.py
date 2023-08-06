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


from types import SimpleNamespace

from ScriptingBridge import SBApplication

from pietunes import core


DEFAULT_LIBRARY_LOCATION = "com.apple.iTunes 'book:1:iTunes Library Location'"


class App(object):
    """The App class provides a Python API for scripting iTunes

    The client application built on this pietunes package should
    instantiate an instance of this class in order to acces the API.
    All messages sent to iTunes should use only the methods provided here.

    Attributes:
        itunes: An SBApplication instance for iTunes.app
        playlists: A dynamically updated list of all playlists known by iTunes
    """

    def __init__(self):
        """Inits App with SBAppication and a list of available playlists."""
        self.itunes = SBApplication.applicationWithBundleIdentifier_(
            "com.apple.iTunes")
        self.playlists = self._get_playlists()

    def _get_playlists(self):
        return list(self.itunes.playlists())

    def get_playlist(self, name):
        """Return a reference to an iTunes Playlist object.

        Args:
            playlist (str): the name of the iTunes playlist

        Returns:
            an iTunes Playlist object
        """
        playlist = None
        candidate = iter(self.playlists)
        while not playlist:
            try:
                p = next(candidate)
                if p.name() == name:
                    playlist = p
                    return playlist
            except StopIteration:
                raise NotFoundError(f'\nNo playlist with the name {name}'
                                    ' could be found.\n')

    def get_sources(self):
        """Returns a list of iTunes data sources.
        """
        return self.itunes.sources()

    def get_tracks(self, playlist):
        """Retrieve the iTunes track objects from the playlist refernce

        Args:
            playlist (str): the name of the playlist that collects the tracks

        Returns:
            an iterator object that yields iTunes track objects
        """
        tracks = (track for track in playlist.tracks())

        return tracks

    def get_track(self, collection, title):
        """Returns an a reference to an iTunes Track object.

        Args:
            collection (generator): a generator object
                                    that yields track objects
            title (str): the title of the track to retrieve

        Returns:
            an iTunes track object
        """
        track = None
        candidate = iter(collection)
        while not track:
            try:
                t = next(candidate)
                if t.name() == title:
                    track = t
                    return track
            except StopIteration:
                raise NotFoundError(f'\nNo movie with the title {title}'
                                    ' could be found.\n')

    def download_track(self, playlist, track):
        """Downloads an iTunes track.

        Args:
            playlist (str): the name of the playlist that contains the track
            track (str): the name of the track to download

        """
        nsargs = SimpleNamespace(
            script='download_track',
            playlist=playlist,
            track=track
        )
        core._call_script(nsargs)

    def open_library(self, location):
        """Open an arbitrary iTunes Library.

        Args:
            location (str): the iTunes Bookmark of the iTunes Library location

        """
        nsargs = SimpleNamespace(script='open_library', location=location)
        core._call_script(nsargs)

    def search(self, playlist, search_text, constraint):
        """Search a playlist for a string, subject to a constraint on the type
        of object to search for.

        Args:
            playlist (str): the name of the iTunes playlist to search
            search_text (str): The text string to search for
            constraint (enum): The subset of objects in the playlist to search
                May be one of:
                    ALBUMS

                    ALL

                    ARTISTS

                    COMPOSERS

                    DISPLAYED

                    SONGS

        Returns:
            a list of objects that at least partially match the search string
        """
        target = self.get_playlist(playlist)
        matches = target.searchFor_only_(search_text, constraint)

        return matches


class NotFoundError(Exception):
    """Error thrown when the item being searched for is not found.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
