from rest_framework.routers import DefaultRouter
from .views import EmailTemplateViewSet, SentEmailViewSet

router = DefaultRouter()

router.register(r'email-template', EmailTemplateViewSet, basename='email-template')
router.register(r'sent-email', SentEmailViewSet, basename='sent-email')

urlpatterns = []
urlpatterns += router.urls
