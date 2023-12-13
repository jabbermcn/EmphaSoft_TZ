from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserLoginSerializer, UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    """View for user registration"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class UserLoginView(TokenObtainPairView):
    """View for user login"""

    serializer_class = UserLoginSerializer
