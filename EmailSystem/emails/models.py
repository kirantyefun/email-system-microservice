from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


# TODO: UserTemplate can be added in future so that user can create their own email templates


class EmailTemplate(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Recipient(models.Model):
    from django.core.validators import validate_email
    email = models.EmailField(unique=True, primary_key=True, validators=[validate_email])

    def __str__(self):
        return self.email


class SentEmail(models.Model):
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    sent_by_email_address = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='sent_emails')
    recipients = models.ManyToManyField(Recipient, related_name='received_emails')
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, blank=True, null=True)
    sent_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject or self.template.subject

    @property
    def email_body(self):
        return self.body or self.template.body



