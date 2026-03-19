from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers

from api.serializers import GenreSerializer

genre_schema = extend_schema_view(
    list=extend_schema(
        summary="Получение списка всех жанров",
        description=(
            "Получить список всех жанров.<br><br>Права доступа: <b>Доступно без токена</b>."
        ),
        auth=[],
        parameters=[
            OpenApiParameter(
                name="search",
                description="Поиск по названию жанра",
                location=OpenApiParameter.QUERY,
            )
        ],
        responses={
            200: OpenApiResponse(response=GenreSerializer, description="Удачное выполнение запроса")
        },
        tags=("GENRES",),
    ),
    create=extend_schema(
        summary="Добавление жанра",
        description=(
            "Добавить жанр.<br><br>"
            "Права доступа: <b>Администратор</b>.<br><br>"
            "Поле `slug` каждого жанра должно быть уникальным."
        ),
        responses={
            201: OpenApiResponse(
                response=GenreSerializer, description="Удачное выполнение запроса"
            ),
            400: OpenApiResponse(
                response=inline_serializer(
                    name="400GenreSerializer",
                    fields={
                        "field_name": serializers.ListField(
                            child=serializers.CharField(), required=False
                        )
                    },
                ),
                description="Отсутсвует обязательное поле или оно некорректно",
            ),
            401: OpenApiResponse(description="Необходим JWT-токен"),
            403: OpenApiResponse(description="Нет прав доступа"),
        },
        tags=("GENRES",),
    ),
    destroy=extend_schema(
        summary="Удаление жанра",
        description=("Удалить жанр.<br><br>Права доступа: <b>Администратор</b>."),
        parameters=[
            OpenApiParameter(
                name="slug",
                description="Slug жанра",
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            204: OpenApiResponse(description="Удачное выполнение запроса"),
            401: OpenApiResponse(description="Необходим JWT-токен"),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Категория не найдена"),
        },
        tags=("GENRES",),
    ),
)
