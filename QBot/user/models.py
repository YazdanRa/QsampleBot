from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    mobile = models.CharField(
        null=True,
        blank=True,
        max_length=16,
        validators=[RegexValidator(regex=r"^(09)\d{9}$")],
    )
    telegram = models.OneToOneField(
        verbose_name="Telegram account",
        to="telegram_bot.TelegramUser",
        on_delete=models.SET_NULL,
        related_name="user",
        null=True,
        blank=True,
    )
