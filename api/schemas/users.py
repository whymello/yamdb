from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers

from api.serializers import UserMeSerializer, UserSerializer

user_schema = extend_schema_view(
    list=extend_schema(
        summary="Получение списка всех пользователей",
        description=(
            "Получить список всех пользователей.<br><br>Права доступа: <b>Администратор</b>."
        ),
        parameters=[
            OpenApiParameter(
                name="search",
                description="Поиск по имени пользователя (username)",
                location=OpenApiParameter.QUERY,
            )
        ],
        responses={
            200: OpenApiResponse(response=UserSerializer, description="Удачное выполнение запроса"),
            401: OpenApiResponse(description="Необходим JWT-токен"),
        },
        tags=("USERS",),
    ),
    create=extend_schema(
        summary="Добавление пользователя",
        description=(
            "Добавить нового пользователя.<br><br>"
            "Права доступа: <b>Администратор</b>.<br><br>"
            "Поля `email` и `username` должны быть уникальными."
        ),
        responses={
            201: OpenApiResponse(response=UserSerializer, description="Удачное выполнение запроса"),
            400: OpenApiResponse(
                response=inline_serializer(
                    name="400UserSerializer",
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
        tags=("USERS",),
    ),
    retrieve=extend_schema(
        summary="Получение пользователя по username",
        description=(
            "Получить пользователя по username.<br><br>Права доступа: <b>Администратор</b>."
        ),
        parameters=[
            OpenApiParameter(
                name="username",
                description="Username пользователя",
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: OpenApiResponse(response=UserSerializer, description="Удачное выполнение запроса"),
            401: OpenApiResponse(description="Необходим JWT-токен"),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Пользователь не найден"),
        },
        tags=("USERS",),
    ),
    partial_update=extend_schema(
        summary="Изменение данных пользователя по username",
        description=(
            "Изменить данные пользователя по username.<br><br>"
            "Права доступа: <b>Администратор</b>.<br><br>"
            "Поля `email` и `username` должны быть уникальными."
        ),
        parameters=[
            OpenApiParameter(
                name="username",
                description="Username пользователя",
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: OpenApiResponse(response=UserSerializer, description="Удачное выполнение запроса"),
            400: OpenApiResponse(
                response=inline_serializer(
                    name="400UserSerializer",
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
            404: OpenApiResponse(description="Пользователь не найден"),
        },
        tags=("USERS",),
    ),
    destroy=extend_schema(
        summary="Удаление пользователя по username",
        description="Удалить пользователя по username.<br><br>Права доступа: <b>Администратор</b>.",
        parameters=[
            OpenApiParameter(
                name="username",
                description="Username пользователя",
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            204: OpenApiResponse(description="Удачное выполнение запроса"),
            401: OpenApiResponse(description="Необходим JWT-токен"),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Пользователь не найден"),
        },
        tags=("USERS",),
    ),
)


userme_schema = extend_schema_view(
    get=extend_schema(
        summary="Получение данных своей учетной записи",
        description=(
            "Получить данные своей учетной записи.<br><br>"
            "Права доступа: <b>Любой авторизованный пользователь</b>."
        ),
        responses={
            200: OpenApiResponse(
                response=UserMeSerializer, description="Удачное выполнение запроса"
            )
        },
        tags=("USERS",),
    ),
    patch=extend_schema(
        summary="Изменение данных своей учетной записи",
        description=(
            "Изменить данные своей учетной записи.<br><br>"
            "Права доступа: <b>Любой авторизованный пользователь</b>.<br><br>"
            "Поля `email` и `username` должны быть уникальными."
        ),
        responses={
            200: OpenApiResponse(
                response=UserMeSerializer, description="Удачное выполнение запроса"
            ),
            400: OpenApiResponse(
                response=inline_serializer(
                    name="400UserMeSerializer",
                    fields={
                        "field_name": serializers.ListField(
                            child=serializers.CharField(), required=False
                        )
                    },
                ),
                description="Отсутсвует обязательное поле или оно некорректно",
            ),
        },
        tags=("USERS",),
    ),
)
