from .serializers import (
    UserSignupSerializer,
    UserLoginSerializer,
    SubscriptionSerializer,
)
from .models import Subscription
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated


def get_token_for_user(user):
    """
    Generates an authentication token for a given user.

    This function generates an authentication token for the specified user using the
     "RefreshToken" class from the django-rest-framework-simplejwt" library.

    Args:
        user: The user object for which the token is generated.

    Returns:
        A dictionary containing the refresh token and access token as strings.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }


class UserSignupView(APIView):
    """
    Handles user signup requests.

    This class defines the behavior for handling user signup requests. It receives a POST request with user data,
    validates it, and creates a new user if the data is valid.

    Args:
        request: The HTTP request object.

    Returns:
        A Response object with the registration result and an authentication token if successful.
    """
    def post(self, request):
        try:
            serializer = UserSignupSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            user = serializer.save()
            token = get_token_for_user(user)
            return Response({'msg': 'Register Successful', 'token': token}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class UserLoginView(APIView):
    """
    Handles user login requests.

    This class defines the behavior for handling user login requests. It receives a POST request with user credentials,
    validates them, and returns a response indicating the success or failure of the login attempt.

    Args:
        request: The HTTP request object.

    Returns:
        A Response object with the login result and an authentication token if successful.

    """
    def post(self, request):
        try:
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
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class SubscriptionView(APIView):
    """
    Handles user subscription requests.

    This class defines the behavior for handling user subscription requests.
    It receives a POST request with subscription data, validates it,
    and creates a new subscription if the data is valid and the user has not
    already subscribed to the specified group.

    Args:
        request: The HTTP request object.

    Returns:
        A Response object with the subscription result.

    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            gc_name = request.data.get('gc_name')
            if Subscription.objects.filter(gc_name=gc_name,user=user).exists():
                return Response({'msg': f'You have already subscribed to {gc_name} group'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = SubscriptionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response({'msg': f'You have successfully subscribed to {gc_name} group'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
