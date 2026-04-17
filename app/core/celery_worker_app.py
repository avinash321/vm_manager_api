from celery import Celery
import os
from app.core.config import REDIS_URL

celery_app = Celery(
    "vm_manager",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# Optional configs
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=False,
    broker_use_ssl={"ssl_cert_reqs": "none"},
    redis_backend_use_ssl={"ssl_cert_reqs": "none"},
    broker_pool_limit=1,
    include=["app.tasks.email_tasks"]
)

print("Celeray App Initiated")
