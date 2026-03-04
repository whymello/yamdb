from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, generics, permissions, status, views, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from users import models

from .permissions import CustomIsAdminUser
from .serializers import SignupSerializer, TokenSerializer, UserMeSerializer, UserSerializer

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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = (CustomIsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("=username",)
    http_method_names = ("get", "post", "patch", "delete", "head", "options")


class UserAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserMeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self) -> models.User:
        return self.request.user
