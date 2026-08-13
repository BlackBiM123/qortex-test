"""Единый формат ошибок API.

Согласно specs/001-music-catalog/spec.md (FR-15): любая ошибка возвращается
как {"detail": "...", "errors": {...}} с корректным HTTP-статусом.
"""

from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.http import Http404
from rest_framework import exceptions as drf_exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def api_exception_handler(exc, context):
    if isinstance(exc, ProtectedError):
        protected_objects = list(exc.protected_objects)
        albums = sorted({str(obj.album) for obj in protected_objects})
        return Response(
            {
                "detail": "Невозможно удалить: объект используется в других записях.",
                "errors": {"albums": albums},
            },
            status=status.HTTP_409_CONFLICT,
        )

    if isinstance(exc, IntegrityError):
        return Response(
            {
                "detail": "Нарушено ограничение целостности данных.",
                "errors": {"non_field_errors": [str(exc)]},
            },
            status=status.HTTP_409_CONFLICT,
        )

    if isinstance(exc, (Http404, PermissionDenied)):
        exc = (
            drf_exceptions.NotFound()
            if isinstance(exc, Http404)
            else drf_exceptions.PermissionDenied()
        )

    response = drf_exception_handler(exc, context)
    if response is None:
        return None

    if isinstance(response.data, dict) and "detail" in response.data and len(response.data) == 1:
        response.data = {"detail": response.data["detail"], "errors": {}}
    elif isinstance(response.data, dict):
        response.data = {"detail": "Ошибка валидации.", "errors": response.data}
    elif isinstance(response.data, list):
        response.data = {
            "detail": "Ошибка валидации.",
            "errors": {"non_field_errors": response.data},
        }

    return response
