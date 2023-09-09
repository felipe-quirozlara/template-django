from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import create_user_client, login_user

router = DefaultRouter()

urlpatterns = [
    path('create-user/', create_user_client, name="Crear usuario cliente"),
    path('login/', login_user, name="Login user"),
]