from __future__ import annotations
from .celery_app import app as celery_app  # noqa: F401

__all__ = ["celery_app"]