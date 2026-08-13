"""Тесты инвариантов модели (см. specs/001-music-catalog/data-model.md)."""

import pytest
from django.db import IntegrityError, connection
from django.db.models import ProtectedError

from catalog.tests.factories import AlbumFactory, AlbumTrackFactory, SongFactory

pytestmark = pytest.mark.django_db

requires_deferrable_constraints = pytest.mark.skipif(
    connection.vendor == "sqlite",
    reason=(
        "SQLite не поддерживает deferrable unique constraints (см. data-model.md); "
        "ограничение проверяется в CI на PostgreSQL."
    ),
)


def test_song_can_belong_to_multiple_albums_with_different_positions():
    """Инвариант 1: переиспользование песни разрешено."""
    song = SongFactory()
    album_a = AlbumFactory()
    album_b = AlbumFactory()

    track_a = AlbumTrackFactory(album=album_a, song=song, position=1)
    track_b = AlbumTrackFactory(album=album_b, song=song, position=5)

    assert track_a.position == 1
    assert track_b.position == 5
    assert set(song.albums.all()) == {album_a, album_b}


@requires_deferrable_constraints
@pytest.mark.django_db(transaction=True)
def test_duplicate_position_in_same_album_is_rejected():
    """Инвариант 2.

    uniq_position_per_album объявлен DEFERRED (см. data-model.md): проверка
    срабатывает не на INSERT, а на COMMIT транзакции. Обычный тест
    pytest-django оборачивает тело в savepoint и никогда не коммитит его
    по-настоящему, поэтому здесь нужен transaction=True — тест выполняется
    в реальных автокоммитящихся транзакциях, как и в проде.
    """
    album = AlbumFactory()
    AlbumTrackFactory(album=album, position=1)

    with pytest.raises(IntegrityError):
        AlbumTrackFactory(album=album, position=1)


def test_duplicate_song_in_same_album_is_rejected():
    """Инвариант 3."""
    album = AlbumFactory()
    song = SongFactory()
    AlbumTrackFactory(album=album, song=song, position=1)

    with pytest.raises(IntegrityError):
        AlbumTrackFactory(album=album, song=song, position=2)


def test_song_used_in_album_cannot_be_deleted():
    """Инвариант 4."""
    song = SongFactory()
    AlbumTrackFactory(song=song)

    with pytest.raises(ProtectedError):
        song.delete()


def test_deleting_album_cascades_tracks_but_not_songs():
    """Инвариант 5."""
    song = SongFactory()
    album = AlbumFactory()
    AlbumTrackFactory(album=album, song=song)

    album.delete()

    song.refresh_from_db()
    assert song.track_entries.count() == 0


def test_unused_song_can_be_deleted():
    song = SongFactory()
    song.delete()
