from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="почта", help_text="Введите почту"
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="аватар",
        blank=True,
        null=True,
        help_text="Загрузите аватар",
    )
    country = models.CharField(
        max_length=35,
        verbose_name="страна",
        blank=True,
        null=True,
        help_text="Введите название страны",
    )
    token = models.CharField(
        max_length=100, verbose_name="token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_view_user", "Может просматривать пользователей"),
            ("can_delete_user", "Может удалить пользователя"),
        ]

    def __str__(self):
        return self.email

    @staticmethod
    def make_random_password(length=8):
        characters = string.ascii_letters + string.digits + string.punctuation
        return "".join(random.choice(characters) for _ in range(length))
