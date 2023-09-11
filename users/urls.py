from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView, TokenVerifyView

from .views import create_user_client, login_user

router = DefaultRouter()

urlpatterns = [
    path('create-user/', create_user_client, name="Crear usuario cliente"),
    path('login/', login_user, name="Login user"),
    # path('private-jwt/', name="Private Jwt"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]