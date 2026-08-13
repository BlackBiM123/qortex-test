import factory

from catalog.models import Album, AlbumTrack, Artist, Song


class ArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Artist

    name = factory.Sequence(lambda n: f"Artist {n}")


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Album

    title = factory.Sequence(lambda n: f"Album {n}")
    artist = factory.SubFactory(ArtistFactory)
    year = 2000


class SongFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Song

    title = factory.Sequence(lambda n: f"Song {n}")


class AlbumTrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AlbumTrack

    album = factory.SubFactory(AlbumFactory)
    song = factory.SubFactory(SongFactory)
    position = factory.Sequence(lambda n: n + 1)
