from django.contrib import admin

from .models import Album, AlbumTrack, Artist, Song


class AlbumTrackInline(admin.TabularInline):
    model = AlbumTrack
    extra = 1
    autocomplete_fields = ["song"]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "artist", "year"]
    list_filter = ["year", "artist"]
    search_fields = ["title", "artist__name"]
    autocomplete_fields = ["artist"]
    inlines = [AlbumTrackInline]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    search_fields = ["title"]


@admin.register(AlbumTrack)
class AlbumTrackAdmin(admin.ModelAdmin):
    list_display = ["id", "album", "position", "song"]
    list_filter = ["album"]
    autocomplete_fields = ["album", "song"]
