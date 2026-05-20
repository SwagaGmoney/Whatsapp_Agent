from celery import Celery
from app.config import get_settings

settings = get_settings()

# Celery instance
celery_app = Celery(
    "resume_agent",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

# Auto-discover tasks inside app/workers/
celery_app.autodiscover_tasks(["app.workers"])

# Optional: Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
