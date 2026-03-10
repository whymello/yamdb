from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.manager import BaseManager
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import backends
from rest_framework import filters, generics, mixins, permissions, status, views, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from reviews.models import Category, Comment, Genre, Review, Title
from users import models

from .permissions import CustomIsAdminUser, CustomIsAdminUserOrReadOnly, IsStaffOrOwnerOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleSerializer,
    TokenSerializer,
    UserMeSerializer,
    UserSerializer,
)

User = get_user_model()


class SignupAPIView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request: Request) -> Response:
        serializer = SignupSerializer(data=request.data)
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

    def post(self, request: Request) -> Response:
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token: dict[str, str] = serializer.save()

        return Response(data=token, status=status.HTTP_200_OK)


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = (CustomIsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    permission_classes = (CustomIsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (CustomIsAdminUserOrReadOnly,)
    filter_backends = (backends.DjangoFilterBackend,)
    filterset_fields = ("category__slug", "genre__slug", "name", "year")
    http_method_names = ("get", "post", "patch", "delete", "head", "options")


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsStaffOrOwnerOrReadOnly,)
    http_method_names = ("get", "post", "patch", "delete", "head", "options")

    def get_queryset(self) -> BaseManager[Review]:
        return Review.objects.filter(title=self.kwargs["title_pk"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["title_id"] = self.kwargs["title_pk"]
        return context

    def perform_create(self, serializer) -> None:
        title = get_object_or_404(Title, id=self.kwargs["title_pk"])
        serializer.save(
            author=self.request.user,
            title=title,
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrOwnerOrReadOnly,)
    http_method_names = ("get", "post", "patch", "delete", "head", "options")

    def get_queryset(self) -> BaseManager[Comment]:
        return Comment.objects.filter(review=self.kwargs["review_pk"])

    def perform_create(self, serializer) -> None:
        review = get_object_or_404(Review, id=self.kwargs["review_pk"])
        serializer.save(
            author=self.request.user,
            review=review,
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = (CustomIsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    http_method_names = ("get", "post", "patch", "delete", "head", "options")


class UserAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserMeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self) -> models.User:
        return self.request.user
