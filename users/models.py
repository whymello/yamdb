from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ("user", "Пользователь"),
    ("moderator", "Модератор"),
    ("admin", "Администратор"),
)


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254, verbose_name="email address")
    bio = models.TextField(blank=True)
    role = models.CharField(choices=ROLE_CHOICES, default="user")
