from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers

from api.serializers import ReviewSerializer

review_schema = extend_schema_view(
    list=extend_schema(
        summary="Получение списка всех отзывов",
        description=(
            "Получить список всех отзывов.<br><br>Права доступа: <b>Доступно без токена</b>."
        ),
        parameters=[
            OpenApiParameter(
                name="title_pk",
                description="id произведения",
                type=int,
                location=OpenApiParameter.PATH,
            )
        ],
        auth=[],
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer, description="Удачное выполнение запроса"
            ),
            404: OpenApiResponse(description="Произведение не найдено"),
        },
        tags=("REVIEWS",),
    ),
    create=extend_schema(
        summary="Добавление нового отзыва",
        description=(
            "Добавить новый отзыв. "
            "Пользователь может оставить только один отзыв на произведение.<br><br>"
            "Права доступа: <b>Аутентифицированные пользователи</b>."
        ),
        parameters=[
            OpenApiParameter(
                name="title_pk",
                description="id произведения",
                type=int,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            201: OpenApiResponse(
                response=ReviewSerializer, description="Удачное выполнение запроса"
            ),
            400: OpenApiResponse(
                response=inline_serializer(
                    name="400ReviewSerializer",
                    fields={
                        "field_name": serializers.ListField(
                            child=serializers.CharField(), required=False
                        )
                    },
                ),
                description="Отсутсвует обязательное поле или оно некорректно",
            ),
            401: OpenApiResponse(description="Необходим JWT-токен"),
            404: OpenApiResponse(description="Произведение не найдено"),
        },
        tags=("REVIEWS",),
    ),
    retrieve=extend_schema(
        summary="Полуение отзыва по id",
        description=(
            "Получить отзыв по id для указанного произведения.<br><br>"
            "Права доступа: <b>Доступно без токена</b>."
        ),
        parameters=[
            OpenApiParameter(
                name="title_pk",
                description="id произведения",
                type=int,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="id",
                description="id отзыва",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer, description="Удачное выполнение запроса"
            ),
            404: OpenApiResponse(description="Произведение или отзыв не найдены"),
        },
        tags=("REVIEWS",),
    ),
    partial_update=extend_schema(
        summary="Частичное обновление отзыва по id",
        description=(
            "Частично обновить отзыв по id.<br><br>"
            "Права доступа: <b>Автор отзыва, модератор или администратор.</b>."
        ),
        parameters=[
            OpenApiParameter(
                name="title_pk",
                description="id произведения",
                type=int,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="id",
                description="id отзыва",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer, description="Удачное выполнение запроса"
            ),
            400: OpenApiResponse(
                response=inline_serializer(
                    name="400ReviewSerializer",
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
            404: OpenApiResponse(description="Произведение или отзыв не найдены"),
        },
        tags=("REVIEWS",),
    ),
    destroy=extend_schema(
        summary="Удаление отзыва по id",
        description=(
            "Удалить отзыв по id.<br><br>"
            "Права доступа: <b>Автор отзыва, модератор или администратор.</b>."
        ),
        parameters=[
            OpenApiParameter(
                name="title_pk",
                description="id произведения",
                type=int,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="id",
                description="id отзыва",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            204: OpenApiResponse(description="Удачное выполнение запроса"),
            401: OpenApiResponse(description="Необходим JWT-токен"),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Произведение или отзыв не найдены"),
        },
        tags=("REVIEWS",),
    ),
)
