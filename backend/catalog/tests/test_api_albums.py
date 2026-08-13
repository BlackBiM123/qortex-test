"""Тесты API альбомов — критерии приёмки AC-1..AC-7 из spec.md."""

import pytest
from rest_framework.test import APIClient

from catalog.models import Album, AlbumTrack, Song
from catalog.tests.factories import AlbumFactory, AlbumTrackFactory, ArtistFactory, SongFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


def test_ac1_song_reused_across_albums_with_independent_positions(client):
    artist = ArtistFactory()
    album_a = AlbumFactory(artist=artist, title="Album A")
    album_b = AlbumFactory(artist=artist, title="Album B")

    resp = client.post(
        f"/api/albums/{album_a.id}/tracks/", {"song_title": "X", "position": 1}, format="json"
    )
    assert resp.status_code == 201
    song_id = resp.data["song"]["id"]

    resp = client.post(
        f"/api/albums/{album_b.id}/tracks/", {"song_id": song_id, "position": 5}, format="json"
    )
    assert resp.status_code == 201

    assert Song.objects.filter(pk=song_id).count() == 1
    assert AlbumTrack.objects.filter(song_id=song_id).count() == 2

    track_b_id = resp.data["id"]
    resp = client.delete(f"/api/albums/{album_b.id}/tracks/{track_b_id}/")
    assert resp.status_code == 204
    assert AlbumTrack.objects.filter(album=album_a, song_id=song_id).exists()


def test_ac2_duplicate_position_rejected(client):
    album = AlbumFactory()
    AlbumTrackFactory(album=album, position=1)

    resp = client.post(
        f"/api/albums/{album.id}/tracks/", {"song_title": "New", "position": 1}, format="json"
    )
    assert resp.status_code == 400
    assert album.tracks.count() == 1


def test_ac3_duplicate_song_rejected(client):
    album = AlbumFactory()
    song = SongFactory()
    AlbumTrackFactory(album=album, song=song, position=1)

    resp = client.post(
        f"/api/albums/{album.id}/tracks/", {"song_id": song.id, "position": 2}, format="json"
    )
    assert resp.status_code == 400
    assert album.tracks.count() == 1


def test_ac4_deleting_used_song_returns_409_with_album_list(client):
    album = AlbumFactory(title="Used Here")
    song = SongFactory()
    AlbumTrackFactory(album=album, song=song)

    resp = client.delete(f"/api/songs/{song.id}/")
    assert resp.status_code == 409
    assert "Used Here" in resp.data["errors"]["albums"][0]
    assert Song.objects.filter(pk=song.id).exists()


def test_ac5_reorder_success_and_rejects_invalid_set(client):
    album = AlbumFactory()
    t1 = AlbumTrackFactory(album=album, position=1)
    t2 = AlbumTrackFactory(album=album, position=2)
    t3 = AlbumTrackFactory(album=album, position=3)

    resp = client.post(
        f"/api/albums/{album.id}/tracks/reorder/",
        {"order": [t3.id, t1.id, t2.id]},
        format="json",
    )
    assert resp.status_code == 200
    t1.refresh_from_db()
    t2.refresh_from_db()
    t3.refresh_from_db()
    assert (t3.position, t1.position, t2.position) == (1, 2, 3)

    resp = client.post(
        f"/api/albums/{album.id}/tracks/reorder/", {"order": [t1.id, t2.id]}, format="json"
    )
    assert resp.status_code == 400
    t1.refresh_from_db()
    assert t1.position == 2  # состояние не изменилось


def test_ac6_filters_search_and_pagination(client):
    artist1 = ArtistFactory(name="Pink Floyd")
    artist2 = ArtistFactory(name="Queen")
    AlbumFactory(artist=artist1, title="The Wall", year=1979)
    AlbumFactory(artist=artist1, title="Animals", year=1977)
    AlbumFactory(artist=artist2, title="A Kind of Magic", year=1986)

    resp = client.get(f"/api/albums/?artist={artist1.id}")
    assert resp.data["count"] == 2

    resp = client.get("/api/albums/?year_min=1980")
    assert resp.data["count"] == 1
    assert resp.data["results"][0]["title"] == "A Kind of Magic"

    resp = client.get("/api/albums/?search=wall")
    assert resp.data["count"] == 1

    resp = client.get("/api/albums/?page_size=1")
    assert len(resp.data["results"]) == 1
    assert resp.data["next"] is not None


def test_ac7_song_detail_lists_all_albums_with_position(client):
    song = SongFactory(title="Shared Song")
    album_a = AlbumFactory(title="A")
    album_b = AlbumFactory(title="B")
    AlbumTrackFactory(album=album_a, song=song, position=2)
    AlbumTrackFactory(album=album_b, song=song, position=7)

    resp = client.get(f"/api/songs/{song.id}/")
    assert resp.status_code == 200
    positions = {entry["album_title"]: entry["position"] for entry in resp.data["albums"]}
    assert positions == {"A": 2, "B": 7}


def test_album_crud(client):
    artist = ArtistFactory()
    resp = client.post(
        "/api/albums/",
        {"title": "New Album", "artist": artist.id, "year": 2020},
        format="json",
    )
    assert resp.status_code == 201
    album_id = resp.data["id"]

    resp = client.patch(f"/api/albums/{album_id}/", {"year": 2021}, format="json")
    assert resp.status_code == 200
    assert resp.data["year"] == 2021

    resp = client.delete(f"/api/albums/{album_id}/")
    assert resp.status_code == 204
    assert not Album.objects.filter(pk=album_id).exists()


def test_album_year_out_of_range_rejected(client):
    artist = ArtistFactory()
    resp = client.post(
        "/api/albums/", {"title": "Too Old", "artist": artist.id, "year": 1500}, format="json"
    )
    assert resp.status_code == 400
