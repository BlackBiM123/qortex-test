"""Модели предметной области.

Ключевое архитектурное решение (см. specs/001-music-catalog/data-model.md):
песня (Song) не имеет прямой связи с альбомом. Связь выражена через явную
промежуточную модель AlbumTrack, которая несёт собственный атрибут —
порядковый номер трека в конкретном альбоме. Это единственный способ
корректно смоделировать требование «одна песня в разных альбомах под
разными номерами».
"""

import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Deferrable, UniqueConstraint

MIN_ALBUM_YEAR = 1860


def max_album_year() -> int:
    return datetime.date.today().year + 1


class Artist(models.Model):
    name = models.CharField("Имя", max_length=200, unique=True, db_index=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"

    def __str__(self) -> str:
        return self.name


class Song(models.Model):
    title = models.CharField("Название", max_length=300, db_index=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Песня"
        verbose_name_plural = "Песни"

    def __str__(self) -> str:
        return self.title


class Album(models.Model):
    title = models.CharField("Название", max_length=300)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="albums", verbose_name="Исполнитель"
    )
    year = models.PositiveSmallIntegerField(
        "Год выпуска",
        validators=[MinValueValidator(MIN_ALBUM_YEAR), MaxValueValidator(max_album_year())],
    )
    songs = models.ManyToManyField(
        Song, through="AlbumTrack", related_name="albums", verbose_name="Песни"
    )

    class Meta:
        ordering = ["-year", "title", "id"]
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
        constraints = [
            UniqueConstraint(fields=["artist", "title", "year"], name="uniq_album_per_artist_year"),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.year})"


class AlbumTrack(models.Model):
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name="tracks", verbose_name="Альбом"
    )
    song = models.ForeignKey(
        Song, on_delete=models.PROTECT, related_name="track_entries", verbose_name="Песня"
    )
    position = models.PositiveSmallIntegerField("Номер трека", validators=[MinValueValidator(1)])

    class Meta:
        ordering = ["position"]
        verbose_name = "Трек альбома"
        verbose_name_plural = "Треки альбома"
        constraints = [
            UniqueConstraint(fields=["album", "song"], name="uniq_song_per_album"),
            UniqueConstraint(
                fields=["album", "position"],
                name="uniq_position_per_album",
                deferrable=Deferrable.DEFERRED,
            ),
        ]

    def __str__(self) -> str:
        return f"{self.album} — {self.position}. {self.song}"
