from django.db import IntegrityError, transaction
from rest_framework import serializers

from .models import Album, AlbumTrack, Artist, Song


class ArtistSerializer(serializers.ModelSerializer):
    albums_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Artist
        fields = ["id", "name", "albums_count"]


class SongTrackEntrySerializer(serializers.ModelSerializer):
    """Отображение вхождения песни в конкретный альбом (для страницы песни)."""

    album_id = serializers.IntegerField(source="album.id", read_only=True)
    album_title = serializers.CharField(source="album.title", read_only=True)
    artist_name = serializers.CharField(source="album.artist.name", read_only=True)
    year = serializers.IntegerField(source="album.year", read_only=True)

    class Meta:
        model = AlbumTrack
        fields = ["id", "album_id", "album_title", "artist_name", "year", "position"]


class SongSerializer(serializers.ModelSerializer):
    albums = SongTrackEntrySerializer(source="track_entries", many=True, read_only=True)

    class Meta:
        model = Song
        fields = ["id", "title", "albums"]


class SongLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["id", "title"]


class AlbumTrackSerializer(serializers.ModelSerializer):
    song = SongLiteSerializer(read_only=True)

    class Meta:
        model = AlbumTrack
        fields = ["id", "song", "position"]


class AlbumListSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source="artist.name", read_only=True)
    tracks_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Album
        fields = ["id", "title", "artist", "artist_name", "year", "tracks_count"]


class AlbumDetailSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source="artist.name", read_only=True)
    tracks = AlbumTrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ["id", "title", "artist", "artist_name", "year", "tracks"]


class AlbumWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ["id", "title", "artist", "year"]

    def to_representation(self, instance):
        return AlbumDetailSerializer(instance, context=self.context).data


class AddTrackSerializer(serializers.Serializer):
    """Добавление трека: либо song_id (существующая песня), либо song_title (новая)."""

    song_id = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(), required=False, source="song"
    )
    song_title = serializers.CharField(required=False, max_length=300, trim_whitespace=True)
    position = serializers.IntegerField(required=False, min_value=1)

    def validate(self, attrs):
        song = attrs.get("song")
        song_title = attrs.get("song_title", "").strip() if attrs.get("song_title") else ""
        if not song and not song_title:
            raise serializers.ValidationError(
                "Укажите song_id существующей песни или song_title для новой."
            )
        if song and song_title:
            raise serializers.ValidationError(
                "Укажите либо song_id, либо song_title, но не оба поля."
            )
        return attrs

    def create(self, validated_data):
        album = self.context["album"]
        song = validated_data.get("song")
        song_title = validated_data.get("song_title") or ""
        song_title = song_title.strip()
        position = validated_data.get("position")

        with transaction.atomic():
            if not song:
                song, _ = Song.objects.get_or_create(title=song_title)

            if position is None:
                last = album.tracks.order_by("-position").first()
                position = (last.position + 1) if last else 1

            if album.tracks.filter(song=song).exists():
                raise serializers.ValidationError(
                    {"song_id": "Эта песня уже входит в данный альбом."}
                )
            if album.tracks.filter(position=position).exists():
                raise serializers.ValidationError(
                    {"position": f"Позиция {position} в этом альбоме уже занята."}
                )

            try:
                track = AlbumTrack.objects.create(album=album, song=song, position=position)
            except IntegrityError as exc:
                raise serializers.ValidationError(
                    {"non_field_errors": ["Не удалось добавить трек: конфликт данных."]}
                ) from exc

        return track

    def to_representation(self, instance):
        return AlbumTrackSerializer(instance, context=self.context).data


class UpdateTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumTrack
        fields = ["position"]

    def validate_position(self, value):
        album = self.instance.album
        if album.tracks.exclude(pk=self.instance.pk).filter(position=value).exists():
            raise serializers.ValidationError(f"Позиция {value} в этом альбоме уже занята.")
        return value

    def to_representation(self, instance):
        return AlbumTrackSerializer(instance, context=self.context).data


class ReorderTracksSerializer(serializers.Serializer):
    order = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

    def validate_order(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Список ID треков содержит повторы.")
        return value

    def save(self):
        album = self.context["album"]
        order = self.validated_data["order"]

        existing_ids = set(album.tracks.values_list("id", flat=True))
        if set(order) != existing_ids:
            raise serializers.ValidationError(
                {
                    "order": (
                        "Список должен содержать ровно все треки альбома, "
                        "без пропусков и лишних ID."
                    )
                }
            )

        with transaction.atomic():
            tracks = {t.id: t for t in album.tracks.all()}
            # Шаг 1: временный непересекающийся диапазон позиций, чтобы избежать
            # промежуточного нарушения uniq_position_per_album на SQLite,
            # где DEFERRED-ограничения не поддерживаются (см. data-model.md).
            for track in tracks.values():
                track.position += 1000
            AlbumTrack.objects.bulk_update(tracks.values(), ["position"])

            for index, track_id in enumerate(order, start=1):
                tracks[track_id].position = index
            AlbumTrack.objects.bulk_update(tracks.values(), ["position"])

        return album.tracks.order_by("position")
