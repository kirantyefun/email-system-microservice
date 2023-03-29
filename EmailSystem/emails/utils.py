import pika, json
from .models import SentEmail


def send_email(message, channel: pika.adapters.blocking_connection.BlockingChannel, sent_email: SentEmail):
    """
    Publish a message to the RabbitMQ message broker using the provided channel.

    Args:
        message (dict): A dictionary containing the email message to be sent.
        channel (pika.adapters.blocking_connection.BlockingChannel): A channel to the RabbitMQ message broker.
        sent_email (SentEmail): A SentEmail object that represents the email being sent.

    Returns:
        str or None: Returns None if the message was successfully published to the broker, otherwise an error message
        as a string.
    """
    try:
        channel.basic_publish(
            exchange="",
            routing_key="email",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        # delete removes entries from many-to-many table relating to recipients
        sent_email.delete()
        print(f"caught exception while putting message to rabbitMq")
        return str(err), 500
