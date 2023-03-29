from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegistrationSerializer, UserSerializer


class CustomAuthToken(ObtainAuthToken):
    """
    A custom token authentication endpoint that returns a token key and user email upon successful login.

    This endpoint uses the ObtainAuthToken view from Django REST Framework to authenticate a user's credentials
    (username and password) and return a token for subsequent API requests. In addition, this endpoint returns
    the user's email along with the token.

    Note that this view assumes that the user model has an 'email' attribute.

    Attributes:
        None

    Methods:
        post(request, *args, **kwargs): Authenticates the user's credentials and returns a token key and email.

    Usage:
        To use this endpoint, make a POST request to the URL associated with this view, passing the user's
        credentials in the request body. On successful authentication, this view will return a JSON object
        containing the token key and email. Example:
        {
            "token": "abcdef123456",
            "email": "example@example.com"
        }
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email,
        })


class UserRegistration(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(serializer.data)
            if user:
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        print(request.user)
        print(request.user.auth_token)
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        logout(request)
        return Response({"success": _("Successfully logged out.")},
                        status=status.HTTP_200_OK)

