from django.db import models


class User(models.Model):
    chat_id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    username = models.CharField(max_length=256, null=True, blank=True)
    is_bot = models.BooleanField(default=False)
    language_code = models.CharField(max_length=8, null=True, blank=True)
    date_met = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{} {} (@{})".format(self.first_name, self.last_name, self.username)
