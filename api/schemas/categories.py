from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers

from api.serializers import CategorySerializer

category_schema = extend_schema_view(
    list=extend_schema(
        summary="Получение списка всех категорий",
        description=(
            "Получить список всех категорий.<br><br>Права доступа: <b>Доступно без токена</b>."
        ),
        auth=[],
        parameters=[
            OpenApiParameter(
                name="search",
                description="Поиск по названию категории",
                location=OpenApiParameter.QUERY,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=CategorySerializer, description="Удачное выполнение запроса"
            )
        },
        tags=("CATEGORIES",),
    ),
    create=extend_schema(
        summary="Добавление новой категории",
        description=(
            "Создать категорию.<br><br>"
            "Права доступа: <b>Администратор</b>.<br><br>"
            "Поле `slug` каждой категории должно быть уникальным."
        ),
        responses={
            201: OpenApiResponse(
                response=CategorySerializer, description="Удачное выполнение запроса"
            ),
            400: OpenApiResponse(
                response=inline_serializer(
                    name="400CategorySerializer",
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
        tags=("CATEGORIES",),
    ),
    destroy=extend_schema(
        summary="Удаление категории",
        description=("Удалить категорию.<br><br>Права доступа: <b>Администратор</b>."),
        parameters=[
            OpenApiParameter(
                name="slug",
                description="Slug категории",
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            204: OpenApiResponse(description="Удачное выполнение запроса"),
            401: OpenApiResponse(description="Необходим JWT-токен"),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Категория не найдена"),
        },
        tags=("CATEGORIES",),
    ),
)
