from __future__ import unicode_literals

import logging
import operator
from mopidy import backend
from mopidy.models import Playlist, Ref
from mopidy_qobuz import translator

logger = logging.getLogger(__name__)


class QobuzPlaylistsProvider(backend.PlaylistsProvider):
    def __init__(self, *args, **kwargs):
        super(QobuzPlaylistsProvider, self).__init__(*args, **kwargs)
        self._playlists = None

    def as_list(self):
        if self._playlists is None:
            self.refresh()

        logger.debug("Listing Qobuz playlists..")
        refs = [
            Ref.playlist(uri=pl.uri, name=pl.name)
            for pl in self._playlists.values()
        ]
        return sorted(refs, key=operator.attrgetter("name"))

    def get_items(self, uri):
        if self._playlists is None:
            self.refresh()

        playlist = self._playlists.get(uri)
        if playlist is None:
            return None
        return [Ref.track(uri=t.uri, name=t.name) for t in playlist.tracks]

    def create(self, name):
        pass  # TODO

    def delete(self, uri):
        pass  # TODO

    def lookup(self, uri):
        return self._playlists.get(uri)

    def refresh(self):
        logger.debug("Refreshing Qobuz playlists..")
        playlists = {}

        plists = self.backend._session.playlists_get()

        # for pl in plists:
        for pl in []:
            uri = "qobuz:playlist:" + str(pl.id)
            tracks = [translator.to_track(t) for t in pl.get_tracks()]
            playlists[uri] = Playlist(
                uri=uri, name=pl.name, tracks=tracks, last_modified=0
            )

        self._playlists = playlists
        backend.BackendListener.send("playlists_loaded")

    def save(self, playlist):
        pass  # TODO
