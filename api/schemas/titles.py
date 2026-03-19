from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers

from api.serializers import TitleSerializer

title_schema = extend_schema_view(
    list=extend_schema(
        summary="Получение списка всех произведений",
        description=(
            "Получить список всех объектов.<br><br>Права доступа: <b>Доступно без токена</b>."
        ),
        auth=[],
        parameters=[
            OpenApiParameter(
                name="category",
                description="фильтрует по полю slug категории",
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="genre",
                description="фильтрует по полю slug жанра",
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="name",
                description="фильтрует по названию произведения",
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="year",
                description="фильтрует по году",
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            200: OpenApiResponse(response=TitleSerializer, description="Удачное выполнение запроса")
        },
        tags=("TITLES",),
    ),
    create=extend_schema(
        summary="Добавление произведения",
        description=(
            "Добавить новое произведение.<br><br>"
            "Права доступа: <b>Администратор</b>.<br><br>"
            "Нельзя добавлять произведения, которые еще не вышли "
            "(год выпуска не может быть больше текущего).<br><br>"
            "При добавлении нового произведения требуется указать "
            "уже существующие категорию и жанр."
        ),
        responses={
            201: OpenApiResponse(
                response=TitleSerializer, description="Удачное выполнение запроса"
            ),
            400: OpenApiResponse(
                response=inline_serializer(
                    name="400TitleSerializer",
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
        tags=("TITLES",),
    ),
    retrieve=extend_schema(
        summary="Получение информации о произведении",
        description="Информация о произведении.<br><br>Права доступа: <b>Доступно без токена</b>.",
        parameters=[
            OpenApiParameter(
                name="id",
                description="id объекта",
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=TitleSerializer, description="Удачное выполнение запроса"
            ),
            404: OpenApiResponse(description="Объект не найден"),
        },
        tags=("TITLES",),
    ),
    partial_update=extend_schema(
        summary="Частичное обновление информации о произведении",
        description=(
            "Обновить информацию о произведении.<br><br>Права доступа: <b>Администратор</b>."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="id объекта",
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=TitleSerializer, description="Удачное выполнение запроса"
            ),
            401: OpenApiResponse(description="Необходим JWT-токен"),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Объект не найден"),
        },
        tags=("TITLES",),
    ),
    destroy=extend_schema(
        summary="Удаление произведения",
        description="Удалить произведение.<br><br>Права доступа: <b>Администратор</b>.",
        parameters=[
            OpenApiParameter(
                name="id",
                description="id объекта",
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            204: OpenApiResponse(description="Удачное выполнение запроса"),
            401: OpenApiResponse(description="Необходим JWT-токен"),
            403: OpenApiResponse(description="Нет прав доступа"),
            404: OpenApiResponse(description="Произведение не найдено"),
        },
        tags=("TITLES",),
    ),
)
