from __future__ import annotations
from celery import shared_task
from django.utils import timezone
from .models import TimerSession

@shared_task
def cleanup_old_sessions() -> None:
    cutoff = timezone.now() - timezone.timedelta(days=30)
    TimerSession.objects.filter(end_time__lt=cutoff).delete()