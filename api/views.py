from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.manager import BaseManager
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import backends
from rest_framework import filters, generics, mixins, permissions, status, views, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from . import serializers
from .filters import TitleFilter
from .permissions import CustomIsAdminUser, CustomIsAdminUserOrReadOnly, IsStaffOrOwnerOrReadOnly
from .schemas import auth, categories, comments, genres, reviews, titles, users


class SignupAPIView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    @auth.signup_schema
    def post(self, request: Request) -> Response:
        serializer = serializers.SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, _ = User.objects.get_or_create(**serializer.validated_data)

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject="Ваш код подтверждения для ресурса YaMDb",
            message=f"Ваш код: {confirmation_code}",
            from_email=None,
            recipient_list=[serializer.validated_data["email"]],
        )

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TokenAPIView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    @auth.token_schema
    def post(self, request: Request) -> Response:
        serializer = serializers.TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token: dict[str, str] = serializer.save()

        return Response(data=token, status=status.HTTP_200_OK)


@categories.category_schema
class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = "slug"
    permission_classes = (CustomIsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


@genres.genre_schema
class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field = "slug"
    permission_classes = (CustomIsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


@titles.title_schema
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = (CustomIsAdminUserOrReadOnly,)
    filter_backends = (backends.DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ("get", "post", "patch", "delete")


@reviews.review_schema
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsStaffOrOwnerOrReadOnly,)
    http_method_names = ("get", "post", "patch", "delete")

    def get_queryset(self) -> BaseManager[Review]:
        return Review.objects.filter(title=self.kwargs["title_pk"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["title"] = self.kwargs["title_pk"]
        return context

    def perform_create(self, serializer) -> None:
        title = get_object_or_404(klass=Title, id=self.kwargs["title_pk"])
        serializer.save(
            author=self.request.user,
            title=title,
        )


@comments.comment_schema
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsStaffOrOwnerOrReadOnly,)
    http_method_names = ("get", "post", "patch", "delete")

    def get_queryset(self) -> BaseManager[Comment]:
        return Comment.objects.filter(review=self.kwargs["review_pk"])

    def perform_create(self, serializer) -> None:
        review = get_object_or_404(Review, id=self.kwargs["review_pk"])
        serializer.save(
            author=self.request.user,
            review=review,
        )


@users.user_schema
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = "username"
    permission_classes = (CustomIsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    http_method_names = ("get", "post", "patch", "delete")


@users.userme_schema
class UserAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserMeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ("get", "patch")

    def get_object(self) -> User:
        return self.request.user
