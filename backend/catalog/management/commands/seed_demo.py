"""Наполняет каталог демоданными.

Специально включает песню, входящую в два альбома с разными номерами
трека — это ключевой сценарий предметной области (см. spec.md, US-3),
и он должен быть виден сразу после запуска, без ручного ввода.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Album, AlbumTrack, Artist, Song


class Command(BaseCommand):
    help = "Наполняет базу демонстрационными данными каталога альбомов."

    def add_arguments(self, parser):
        parser.add_argument(
            "--if-empty",
            action="store_true",
            help="Заполнять только если в базе ещё нет ни одного альбома.",
        )

    def handle(self, *args, **options):
        if options["if_empty"] and Album.objects.exists():
            self.stdout.write(self.style.WARNING("Данные уже есть, пропускаю (--if-empty)."))
            return

        with transaction.atomic():
            self._seed()

        self.stdout.write(self.style.SUCCESS("Демоданные загружены."))

    def _seed(self):
        pink_floyd, _ = Artist.objects.get_or_create(name="Pink Floyd")
        queen, _ = Artist.objects.get_or_create(name="Queen")
        muse, _ = Artist.objects.get_or_create(name="Muse")

        dsotm, _ = Album.objects.get_or_create(
            artist=pink_floyd, title="The Dark Side of the Moon", year=1973
        )
        pulse, _ = Album.objects.get_or_create(artist=pink_floyd, title="Pulse (Live)", year=1995)
        anight, _ = Album.objects.get_or_create(
            artist=queen, title="A Night at the Opera", year=1975
        )
        greatest_hits, _ = Album.objects.get_or_create(
            artist=queen, title="Greatest Hits", year=1981
        )
        black_holes, _ = Album.objects.get_or_create(
            artist=muse, title="Black Holes and Revelations", year=2006
        )

        money, _ = Song.objects.get_or_create(title="Money")
        time_song, _ = Song.objects.get_or_create(title="Time")
        breathe, _ = Song.objects.get_or_create(title="Breathe")
        bohemian, _ = Song.objects.get_or_create(title="Bohemian Rhapsody")
        love_of_life, _ = Song.objects.get_or_create(title="Love of My Life")
        starlight, _ = Song.objects.get_or_create(title="Starlight")
        supermassive, _ = Song.objects.get_or_create(title="Supermassive Black Hole")

        tracks = [
            (dsotm, breathe, 2),
            (dsotm, time_song, 4),
            (dsotm, money, 6),
            # Ключевой демо-кейс: "Money" повторно используется в живом альбоме
            # Pulse под другим номером трека — ровно сценарий US-3 из spec.md.
            (pulse, money, 9),
            (pulse, time_song, 7),
            (anight, bohemian, 11),
            (anight, love_of_life, 8),
            (greatest_hits, bohemian, 1),
            (greatest_hits, love_of_life, 2),
            (black_holes, starlight, 1),
            (black_holes, supermassive, 2),
        ]
        for album, song, position in tracks:
            AlbumTrack.objects.get_or_create(
                album=album, song=song, defaults={"position": position}
            )
