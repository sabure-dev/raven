from taskiq_aio_pika import AioPikaBroker

from core.config.config import settings

RABBITMQ_URL = f"amqp://\
{settings.rabbitmq_settings.RABBITMQ_USER}:\
{settings.rabbitmq_settings.RABBITMQ_PASS}@\
{settings.rabbitmq_settings.RABBITMQ_HOST}:\
{settings.rabbitmq_settings.RABBITMQ_PORT}/"

broker = AioPikaBroker(
    url=RABBITMQ_URL,
)
