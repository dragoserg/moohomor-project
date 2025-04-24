from __future__ import annotations
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    users = models.ManyToManyField(User, related_name='achievements', blank=True)

    def __str__(self) -> str:
        return self.title
