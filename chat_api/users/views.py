from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.authtoken.models import Token
from users.serializers import UserSerializer
from core.utils import create_response

class UserViewSet(ModelViewSet):

    """
    Viewset to 
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    renderer_classes = (BrowsableAPIRenderer,)

class LoginView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        if not request.data.get('email'):
            return create_response(
                message="Missing key 'email' in request",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not request.data.get('password'):
            return create_response(
                message="Missing key 'password' in request",
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.filter(email=request.data.get('email'))
        if user.exists():
            user = user.first()
        else:
            return create_response(
                message="Invalid username",
                status=status.HTTP_400_BAD_REQUEST
            )
        if not user.check_password(request.data.get('password')):
            return create_response(
                message="Invalid password",
                status=status.HTTP_400_BAD_REQUEST
            )
        token, created = Token.objects.get_or_create(user=user)
        data = {
            "token": token.key,
            "user_id": user.pk,
            "email": user.email
        }
        return create_response(
            message="Success",
            status=status.HTTP_200_OK,
            data=data
        )

class LogoutView(APIView):

    def get(self, request):
        token = request.auth
        token.delete()
        logout(request)

        return create_response(
            message="Logged out successfully",
            status=status.HTTP_200_OK
        )
