from django.contrib import admin
from .models import EmailTemplate, SentEmail, Recipient


admin.site.register(EmailTemplate, admin.ModelAdmin)
admin.site.register(SentEmail, admin.ModelAdmin)
admin.site.register(Recipient, admin.ModelAdmin)
