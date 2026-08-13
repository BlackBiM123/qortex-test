"""Проверка отсутствия N+1 запросов на списках (constitution.md §3)."""

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from rest_framework.test import APIClient

from catalog.tests.factories import AlbumFactory, AlbumTrackFactory, ArtistFactory

pytestmark = pytest.mark.django_db


def test_album_list_has_constant_query_count_regardless_of_row_count():
    client = APIClient()
    artist = ArtistFactory()
    for _ in range(3):
        AlbumFactory(artist=artist)

    with CaptureQueriesContext(connection) as ctx:
        client.get("/api/albums/")
    queries_for_3 = len(ctx.captured_queries)

    for _ in range(10):
        AlbumFactory(artist=artist)

    with CaptureQueriesContext(connection) as ctx:
        client.get("/api/albums/")
    queries_for_13 = len(ctx.captured_queries)

    assert queries_for_13 == queries_for_3


def test_album_detail_prefetches_tracks_and_songs():
    client = APIClient()
    album = AlbumFactory()
    for i in range(5):
        AlbumTrackFactory(album=album, position=i + 1)

    with CaptureQueriesContext(connection) as ctx:
        client.get(f"/api/albums/{album.id}/")

    assert len(ctx.captured_queries) <= 4
