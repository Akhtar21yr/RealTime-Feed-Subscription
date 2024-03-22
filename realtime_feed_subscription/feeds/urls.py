from django.urls import path
from feeds.views import UserSignupView,UserLoginView

urlpatterns = [
    path('api/register/', UserSignupView.as_view(), name='register'),
    path('api/login/', UserLoginView.as_view(), name='login'),
]
