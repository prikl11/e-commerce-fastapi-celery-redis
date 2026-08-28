from celery import Celery

from app.core.config import settings

celery_app = Celery(include=["app.tasks.orders"], broker=settings.celery_broker_url, backend=settings.celery_result_backend)