from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import AccessToken

from users import models

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ("email", "username")

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        email = attrs.get("email")
        username = attrs.get("username")

        user = User.objects.filter(email=email)

        if user and user[0].username != username:
            raise serializers.ValidationError(
                detail={"email": "Пользователь с таким email address уже существует."},
                code=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(username=username)

        if user and user[0].email != email:
            raise serializers.ValidationError(
                detail={"username": "Пользователь с таким именем уже существует."},
                code=status.HTTP_400_BAD_REQUEST,
            )

        return attrs

    def validate_username(self, value: str) -> str:
        if value.lower() == "me":
            raise serializers.ValidationError(
                detail=f"Использовать значение {value} в качестве имени запрещено.",
                code=status.HTTP_400_BAD_REQUEST,
            )

        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        username = attrs.get("username")
        confirmation_code = attrs.get("confirmation_code")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as exc:
            raise serializers.ValidationError(
                detail={"username": "Пользователь с таким именем не найден."},
                code=status.HTTP_404_NOT_FOUND,
            ) from exc

        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                detail={"confirmation_code": "Неверный код подтверждения."},
                code=status.HTTP_400_BAD_REQUEST,
            )

        attrs["user"] = user

        return attrs

    def create(self, validated_data: dict[str, str | models.User]) -> dict[str, str]:
        user = validated_data.pop("user")
        token = AccessToken.for_user(user=user)

        return {"token": str(token)}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "bio", "role")


class UserMeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)
