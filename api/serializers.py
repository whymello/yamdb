from datetime import date

from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from rest_framework import exceptions, serializers, status
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


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
            raise exceptions.NotFound(
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

    def create(self, validated_data: dict[str, str | User]) -> dict[str, str]:
        user = validated_data.pop("user")
        token = AccessToken.for_user(user=user)

        return {"token": str(token)}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(
        read_only=True, label="Рейтинг на основе отзывов, если отзывов нет — `None`"
    )
    genre = serializers.SlugRelatedField(many=True, slug_field="slug", queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field="slug", queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        read_only_fields = ("id",)

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)
        representation["genre"] = GenreSerializer(instance.genre.all(), many=True).data
        representation["category"] = CategorySerializer(instance.category).data
        return representation

    def get_rating(self, obj: Title) -> None | int:
        reviews = obj.reviews.all()
        avg_score = reviews.aggregate(Avg("score"))["score__avg"]
        return None if avg_score is None else int(avg_score)

    def validate_year(self, value: int) -> int:
        if value > date.today().year:
            raise serializers.ValidationError(
                detail="Нельзя добавлять произведения, которые еще не вышли.",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    MIN_VALUE, MAX_VALUE = 1, 10

    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")
        read_only_fields = ("id", "pub_date")

    def validate_score(self, value: int) -> int:

        if value < self.MIN_VALUE or value > self.MAX_VALUE:
            raise serializers.ValidationError(
                detail="Оценка произведения должна быть в пределах [1..10].",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return value

    def validate(self, attrs: dict[str, str | int]) -> dict[str, str | int]:
        author = self.context["request"].user
        title = self.context["title"]

        if self.instance is None and Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError(
                detail="Вы уже оставляли отзыв на это произведение.",
                code=status.HTTP_400_BAD_REQUEST,
            )

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("id", "pub_date")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "bio", "role")


class UserMeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)
