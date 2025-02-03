from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import Job


class CustomUser(AbstractUser):
    # Add additional fields here
    email = models.EmailField(unique=True)
    favorited_jobs = models.ManyToManyField(
        Job, blank=True, related_name='favorited_by')

    def __str__(self):
        return self.username
