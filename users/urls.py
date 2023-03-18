from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import UserViewSet

app_name = 'users'

user_router = SimpleRouter()
user_router.register(r'users', UserViewSet, basename="users")

urlpatterns = [
    path("", include(user_router.urls)),
]
