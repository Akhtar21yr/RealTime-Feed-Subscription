from .serializers import UserSignupSerializer,UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        token = get_token_for_user(user)
        return Response({'msg': 'Register Successful', 'token': token}, status=status.HTTP_201_CREATED)
    
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                user.last_login = timezone.now().astimezone(timezone.get_current_timezone())
                user.save()
                token = get_token_for_user(user)
                return Response({ "msg": "Login Successful","token": token}, status=status.HTTP_200_OK)
            return Response({"errors": {"validation_errors": ['password and email is not valid']}}, status=status.HTTP_404_NOT_FOUND)
