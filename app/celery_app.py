from celery import Celery
import os

# Configuração do Broker e do Backend
broker_url = os.environ.get("CELERY_BROKER_URL", "amqp://rabbitmq:5672")
result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")

# Configurando a aplicação Celery
celery_app = Celery(
    "celery_app",
    broker=broker_url,
    backend=result_backend,
    include=["app.tasks"],
)

# Atualizações de configuração adicionais, se necessário
celery_app.conf.update(
    task_routes={"app.tasks.*": {"queue": "default"}},
    task_default_queue="default",
    broker_connection_retry_on_startup=True,
)
