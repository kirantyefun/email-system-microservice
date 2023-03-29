from rest_framework import serializers
from .models import EmailTemplate, SentEmail


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = "__all__"


class SentEmailSerializer(serializers.ModelSerializer):
    sent_by_email_address = serializers.SerializerMethodField()

    class Meta:
        model = SentEmail
        fields = '__all__'
        read_only_fields = ('sent_time', 'recipients')

    def get_sent_by_email_address(self, obj):
        return obj.sent_by_email_address.email

    def create(self, validated_data):
        validated_data['sent_by_email_address'] = self.context['request'].user
        return super().create(validated_data)

