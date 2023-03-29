from typing import List

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from .models import EmailTemplate, Recipient, SentEmail
from django.contrib.auth import get_user_model
from .serializers import EmailTemplateSerializer, SentEmailSerializer
from rest_framework import permissions

import pika
from . import utils


# TODO: externalize rate value to config files

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


UserModel = get_user_model()


class TenPerDayThrottle(UserRateThrottle):
    rate = '10/day'


def filter_qs_helper(request, qs, fields):
    """
    Helper function to filter a queryset based on the given fields.

    Args:
        request (HttpRequest): The request object containing the query parameters.
        qs (QuerySet): The queryset to be filtered.
        fields (Tuple[str, str]]): A list of tuples containing the query parameter name and the corresponding model field.

    Returns:
        QuerySet: The filtered queryset.
    """
    for param, field in fields:
        val = request.query_params.get(param)
        if param == "recipient":
            val = request.GET.getlist(param, [])
        if val:
            print('value found')
            print(f'param: {param} :: value:; {val} :: field:: {field}')
            qs = qs.filter(**{field: val})
    qs = qs.all()
    return qs


class EmailTemplateViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer


class SentEmailViewSet(viewsets.ModelViewSet):
    serializer_class = SentEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return a queryset of SentEmail objects filtered by the current user and optional query parameters.
        """
        queryset = self.request.user.sent_emails.select_related('template')
        if self.action == 'list':
            fields = (
                ('recipient', 'recipients__in'),
                ('start_time', 'sent_time__gte'),
                ('end_time', 'sent_time__lte')
            )
            queryset = filter_qs_helper(self.request, queryset, fields)
        return queryset

    def get_throttles(self):
        throttle_classes = []
        if self.action == "create":
            throttle_classes = [TenPerDayThrottle]
        return [throttle() for throttle in throttle_classes]

    def create(self, request, *args, **kwargs):
        """
        Create a single sent_email instance.
        Create new instances of Recipient in bulk if not already present in DB.
        Associate sent_email instance with instances of Recipient
        """
        recipient_emails = request.data.pop('recipients', [])
        if not isinstance(recipient_emails, List):
            return Response(
                {
                    "error_message": "Recipient Emails need to be in form of a list"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        sent_email_serializer = self.get_serializer(data=request.data)
        sent_email_serializer.is_valid(raise_exception=True)
        sent_email: SentEmail = sent_email_serializer.save(sent_by_email_address=request.user)

        existing_recipients = Recipient.objects.filter(email__in=recipient_emails).values_list('email', flat=True)
        recipients_to_create = [Recipient(email=email.strip()) for email in recipient_emails if email not in existing_recipients]
        Recipient.objects.bulk_create(recipients_to_create)
        sent_email.recipients.set(Recipient.objects.filter(email__in=recipient_emails))
        err = utils.send_email({
            "from_email": request.user.email,
            "to_emails": recipient_emails,
            "subject": sent_email.__str__(),
            "html_content": sent_email.email_body
        }, channel, sent_email)
        if err:
            return Response(
                {
                    "error_message": err[0]
                }
            )
        return Response(
            {
                "message": "Email sent. It might take a while to deliver."
            }
        )

    def update(self, request, *args, **kwargs):
        """
        Throw 405 error status code for put request
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        """
        Throw 405 error status code for patch request
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        """
        Throw 405 error status code for delete request
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)




