from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import saludo, saludo_private, get_all_products

router = DefaultRouter()

urlpatterns = [
    path('saludo/', saludo, name="Saludo Input"),
    path('private-saludo/', saludo_private, name='Saludo para users privados'),
    path('products/', get_all_products, name="Get all products"),
]