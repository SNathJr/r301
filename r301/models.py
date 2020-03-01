from django.db import models
from django.contrib.auth.models import User

class URLMap(models.Model):
    short_url = models.CharField(unique=True, max_length=256)
    long_url = models.CharField(max_length=1024)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.short_urls} -> {self.long_url}"