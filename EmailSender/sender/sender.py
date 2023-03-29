from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# TODO: write code for consuming from notification queue as well and send another email as notification to the sender


def send_email(body):
    """
    Send an email message using the SendGrid API.

    Args:
        body (dict): A dictionary representing the email message, including the following fields:
            - to: A list of email addresses for the message recipients.
            - from_email: The email address of the message sender.
            - subject: The subject of the message.
            - html_content: The HTML content of the message.

    Returns:
        If the email message is sent successfully, this function does not return any value. Otherwise,
        it returns a string containing an error message.

    Raises:
        SendGridException: If an error occurs while sending the email message.
    """
    message = Mail(**body)
    try:
        sg = SendGridAPIClient('Your SendGrid API key here')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

        # uncomment when notification queue and its consumer is ready
        # try:
        #     channel.basic_publish(
        #         exchange="",
        #         routing_key="notification",
        #         body=json.dumps({
        #             "email_sent": True
        #         }),
        #         properties=pika.BasicProperties(
        #             delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        #         ),
        #     )
        # except Exception as err:
        #     print("Failed to publish message. Email Sent nevertheless")
        #     pass
    except Exception as e:
        print(str(e))
        return str(e)
