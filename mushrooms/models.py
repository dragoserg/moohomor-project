from __future__ import annotations
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name

class MushroomSpecies(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

class Mushroom(models.Model):
    STAGE_SMALL = 'small'
    STAGE_MEDIUM = 'medium'
    STAGE_BIG = 'big'

    STAGES = [
        (STAGE_SMALL, 'Маленький'),
        (STAGE_MEDIUM, 'Средний'),
        (STAGE_BIG, 'Большой'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mushrooms')
    species = models.ForeignKey(MushroomSpecies, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    growth_stage = models.CharField(max_length=6, choices=STAGES, default=STAGE_SMALL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.species.name} ({self.get_growth_stage_display()})"

class TimerSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    species = models.ForeignKey(MushroomSpecies, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    duration = models.PositiveIntegerField(help_text='Длительность в минутах', editable=False)

    def save(self, *args, **kwargs):
        self.duration = int((self.end_time - self.start_time).total_seconds() // 60)
        super().save(*args, **kwargs)
        self._create_or_update_mushroom()

    def _create_or_update_mushroom(self) -> None:
        if self.duration <= 30:
            stage = Mushroom.STAGE_SMALL
        elif self.duration <= 60:
            stage = Mushroom.STAGE_MEDIUM
        else:
            stage = Mushroom.STAGE_BIG
        Mushroom.objects.create(
            user=self.user,
            species=self.species,
            tag=self.tag,
            growth_stage=stage,
        )