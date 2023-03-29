import pika, sys, os, json
from pika.adapters.blocking_connection import BlockingChannel

from sender import sender


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    def callback(ch: BlockingChannel, method, properties, body):
        """
        A callback function to be called when a message is received from the RabbitMQ message broker.

        Args:
            ch (BlockingChannel): The channel on which the message was received.
            method: Contains the message delivery information.
            properties: Contains the message properties.
            body (bytes): The message body in JSON format.

        Returns:
            None: This function does not return anything.
            """
        err = sender.send_email(json.loads(body))
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        "email",
        on_message_callback=callback
    )

    print("waiting for messages. To exit, press Ctrl+c")
    channel.start_consuming()


try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    print("Interrupted")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
