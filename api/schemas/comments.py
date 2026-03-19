from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers

from api.serializers import CommentSerializer

comment_schema = extend_schema_view(
    list=extend_schema(
        summary="Получение списка всех комментариев к отзыву",
        description=(
            "Получить список всех комментариев к отзыву по id."
            "<br><br>Права доступа: <b>Доступно без токена</b>."
        ),
        parameters=[
            OpenApiParameter(
                name="title_pk",
                description="id произведения",
                type=int,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="review_pk",
                description="id отзыва",
                type=int,
                location=OpenApiParameter.PATH,
            ),
        ],
        auth=[],
        responses={
            200: OpenApiResponse(
                response=CommentSerializer, description="Удачное выполнение запроса"
            ),
            404: OpenApiResponse(description="Произведение или отзыв не найдены"),
        },
        tags=("COMMENTS",),
    ),
    create=extend_schema(
        summary="Добавление комментария к отзыву",
        description=(
            "Добавить новый комментарий для отзыва.<br><br>"
            "Права доступа: <b>Аутентифицированные пользователи</b>."
        ),
        parameters=[
            OpenApiParameter(
                name="title_pk",
                description="id произведения",
                type=int,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="review_pk",
                description="id отзыва",
                type=int,
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            201: OpenApiResponse(
                response=CommentSerializer, description="Удачное выполнение запроса"
            ),
            400: OpenApiResponse(
                response=inline_serializer(
                    name="400CommentSerializer",
                    fields={
                        "field_name": serializers.ListField(
                            child=serializers.CharField(), required=False
                        )
                    },
                ),
                description="Отсутсвует обязательное поле или оно некорректно",
            ),
            401: OpenApiResponse(description="Необходим JWT-токен"),
            404: OpenApiResponse(description="Произведение или отзыв не найдены"),
        },
        tags=("COMMENTS",),
    ),
    retrieve=extend_schema(
        summary="Получение комментария к отзыву",
        description=(
            "Получить комментарий для отзыва по id.<br><br>"
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
                name="review_pk",
                description="id отзыва",
                type=int,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="id",
                description="id комментария",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=CommentSerializer, description="Удачное выполнение запроса"
            ),
            404: OpenApiResponse(description="Произведение, отзыв или комментарий не найдены"),
        },
        tags=("COMMENTS",),
    ),
    partial_update=extend_schema(
        summary="Частичное обновление комментария к отзыву",
        description=(
            "Частично обновить комментарий к отзыву по id.<br><br>"
            "Права доступа: <b>Автор комментария, модератор или администратор.</b>."
        ),
        parameters=[
            OpenApiParameter(
                name="title_pk",
                description="id произведения",
                type=int,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="review_pk",
                description="id отзыва",
                type=int,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="id",
                description="id комментария",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=CommentSerializer, description="Удачное выполнение запроса"
            ),
            400: OpenApiResponse(
                response=inline_serializer(
                    name="400CommentSerializer",
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
            404: OpenApiResponse(description="Произведение, отзыв или комментарий не найдены"),
        },
        tags=("COMMENTS",),
    ),
    destroy=extend_schema(
        summary="Удаление комментария к отзыву",
        description=(
            "Удалить комментарий к отзыву по id.<br><br>"
            "Права доступа: <b>Автор комментария, модератор или администратор.</b>."
        ),
        parameters=[
            OpenApiParameter(
                name="title_pk",
                description="id произведения",
                type=int,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="review_pk",
                description="id отзыва",
                type=int,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="id",
                description="id комментария",
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            204: OpenApiResponse(description="Удачное выполнение запроса"),
            401: OpenApiResponse(description="Необходим JWT-токен"),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Произведение, отзыв или комментарий не найдены"),
        },
        tags=("COMMENTS",),
    ),
)
