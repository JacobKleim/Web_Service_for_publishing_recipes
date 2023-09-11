from django.contrib.auth.models import AbstractUser
from django.db.models import F, CheckConstraint
from django.db import models


LENGTH = 150
LENGTH_EMAIL = 254


class User(AbstractUser):
    username = models.CharField(max_length=LENGTH, unique=True)
    email = models.EmailField(max_length=LENGTH_EMAIL, unique=True)
    first_name = models.CharField(max_length=LENGTH)
    last_name = models.CharField(max_length=LENGTH)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписки на автора рецепта"""
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name="Подписчик",
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        verbose_name="Автор",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='user_author'
            ),
            CheckConstraint(
                check=~models.Q(user=F('following')),
                name='no_self_follow'
            )
        ]

    def __str__(self) -> str:
        return f'{self.user} {self.following}'
