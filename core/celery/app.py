from celery import Celery

from core.config import settings

celery_app = Celery(
    "nepal_legal_rag",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_soft_time_limit=settings.celery_task_soft_time_limit,
    task_time_limit=settings.celery_task_time_limit,
    broker_connection_retry_on_startup=True,
)
