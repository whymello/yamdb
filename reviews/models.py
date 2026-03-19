from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):
    name = models.CharField(verbose_name="Название")
    year = models.PositiveSmallIntegerField(verbose_name="Год выпуска")
    description = models.TextField(verbose_name="Описание", blank=True)
    genre = models.ManyToManyField(to=Genre, related_name="titles")
    category = models.ForeignKey(
        to=Category, on_delete=models.SET_NULL, null=True, related_name="titles"
    )


class Review(models.Model):
    title = models.ForeignKey(to=Title, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="reviews")
    score = models.PositiveSmallIntegerField(verbose_name="Оценка")
    pub_date = models.DateTimeField(verbose_name="Дата публикации отзыва", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("title", "author"),
                name="unique_review_per_user_per_title",
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(verbose_name="Текст комментария")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField(verbose_name="Дата публикации комментария", auto_now_add=True)
