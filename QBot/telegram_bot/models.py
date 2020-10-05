from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    chat_id = models.CharField(max_length=128, unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, null=True)
    username = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return "{} {} (@{})".format(self.first_name, self.last_name, self.username)
