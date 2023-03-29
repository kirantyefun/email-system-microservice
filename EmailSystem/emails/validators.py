from django.core.validators import EmailValidator


def validate_email(value):
    email_validator = EmailValidator("Invalid email address.")
    email_validator(value)
