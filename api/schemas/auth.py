from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers

from api.serializers import SignupSerializer, TokenSerializer

signup_schema = extend_schema(
    summary="Регистрация нового пользователя",
    description=(
        "Получить код подтверждения на переданный `email`.<br><br>"
        "Права доступа: <b>Доступно без токена</b>.<br><br>"
        "Использовать имя 'me' в качестве `username` запрещено.<br><br>"
        "Поля `email` и `username` должны быть уникальными."
    ),
    auth=[],
    request=SignupSerializer,
    responses={
        200: OpenApiResponse(response=SignupSerializer, description="Удачное выполнение запроса"),
        400: OpenApiResponse(
            response=inline_serializer(
                name="400SignupSerializer",
                fields={
                    "field_name": serializers.ListField(
                        child=serializers.CharField(), required=False
                    )
                },
            ),
            description="Отсутсвует обязательное поле или оно некорректно",
        ),
    },
    tags=("AUTH",),
)


token_schema = extend_schema(
    summary="Получение JWT-токена",
    description=(
        "Получение JWT-токена в обмен на username и confirmation code.<br><br>"
        "Права доступа: <b>Доступно без токена</b>."
    ),
    auth=[],
    request=TokenSerializer,
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="200TokenSerializer",
                fields={"token": serializers.CharField(label="access токен", required=False)},
            ),
            description="Удачное выполнение запроса",
        ),
        400: OpenApiResponse(
            response=inline_serializer(
                name="400TokenSerializer",
                fields={
                    "field_name": serializers.ListField(
                        child=serializers.CharField(), required=False
                    )
                },
            ),
            description="Отсутсвует обязательное поле или оно некорректно",
        ),
        404: OpenApiResponse(description="Пользователь не найден"),
    },
    tags=("AUTH",),
)
