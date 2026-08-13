import django_filters as filters

from .models import Album


class AlbumFilter(filters.FilterSet):
    artist = filters.NumberFilter(field_name="artist_id")
    year = filters.NumberFilter(field_name="year")
    year_min = filters.NumberFilter(field_name="year", lookup_expr="gte")
    year_max = filters.NumberFilter(field_name="year", lookup_expr="lte")

    class Meta:
        model = Album
        fields = ["artist", "year", "year_min", "year_max"]
