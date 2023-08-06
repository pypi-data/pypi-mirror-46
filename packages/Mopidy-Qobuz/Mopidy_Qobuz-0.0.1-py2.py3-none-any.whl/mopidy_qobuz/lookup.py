from __future__ import unicode_literals

import logging

import qobuz

from mopidy_qobuz import translator


logger = logging.getLogger(__name__)


def lookup(uri):
    parts = uri.split(":")

    if uri.startswith("qobuz:track:"):
        return [qobuz.Track.from_id(parts[3])]

    if uri.startswith("qobuz:album"):
        return [a.tracks for a in qobuz.Album.from_id(parts[2])]

    logger.info('Failed to lookup "%s"', uri)
