from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="reviews")
    score = models.PositiveSmallIntegerField(verbose_name="Оценка")
    pub_date = models.DateTimeField(verbose_name="Дата публикации отзыва", auto_now_add=True)
    title = models.ForeignKey(to=Title, on_delete=models.CASCADE, related_name="reviews")


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField(verbose_name="Дата публикации комментария", auto_now_add=True)
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, related_name="comments")
