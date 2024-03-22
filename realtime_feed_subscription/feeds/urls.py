# realtime_feed_subscription/urls.py

from django.urls import path
from feeds.views import UserSignupView


urlpatterns = [
    path('api/register/', UserSignupView.as_view(), name='register'),
]
