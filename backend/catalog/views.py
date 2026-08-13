from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import AlbumFilter
from .models import Album, Artist, Song
from .serializers import (
    AddTrackSerializer,
    AlbumDetailSerializer,
    AlbumListSerializer,
    AlbumTrackSerializer,
    AlbumWriteSerializer,
    ArtistSerializer,
    ReorderTracksSerializer,
    SongSerializer,
    UpdateTrackSerializer,
)


class ArtistViewSet(viewsets.ModelViewSet):
    serializer_class = ArtistSerializer
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        return Artist.objects.annotate(albums_count=Count("albums")).order_by("name", "id")


class SongViewSet(viewsets.ModelViewSet):
    serializer_class = SongSerializer
    search_fields = ["title"]
    ordering_fields = ["title"]

    def get_queryset(self):
        return Song.objects.prefetch_related("track_entries__album__artist").order_by("title")


class AlbumViewSet(viewsets.ModelViewSet):
    filterset_class = AlbumFilter
    search_fields = ["title", "artist__name"]
    ordering_fields = ["year", "title"]

    def get_queryset(self):
        qs = Album.objects.select_related("artist")
        if self.action == "list":
            # annotate() с агрегатом (GROUP BY) сбрасывает ORDER BY по умолчанию из Meta —
            # его нужно применить явно, иначе пагинация становится недетерминированной.
            qs = qs.annotate(tracks_count=Count("tracks")).order_by(*Album._meta.ordering)
        else:
            qs = qs.prefetch_related("tracks__song")
        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return AlbumListSerializer
        if self.action in ("create", "update", "partial_update"):
            return AlbumWriteSerializer
        return AlbumDetailSerializer

    @action(detail=True, methods=["post"], url_path="tracks")
    def add_track(self, request, pk=None):
        album = self.get_object()
        serializer = AddTrackSerializer(
            data=request.data, context={"album": album, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        track = serializer.save()
        return Response(AlbumTrackSerializer(track).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch", "delete"], url_path=r"tracks/(?P<track_id>\d+)")
    def track_detail(self, request, pk=None, track_id=None):
        album = self.get_object()
        track = get_object_or_404(album.tracks.select_related("song"), pk=track_id)

        if request.method == "DELETE":
            track.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = UpdateTrackSerializer(track, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="tracks/reorder")
    def reorder_tracks(self, request, pk=None):
        album = self.get_object()
        serializer = ReorderTracksSerializer(data=request.data, context={"album": album})
        serializer.is_valid(raise_exception=True)
        tracks = serializer.save()
        return Response(AlbumTrackSerializer(tracks, many=True).data)
