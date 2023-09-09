import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse

from .models import Product
from .serializer import ProductSerializer


@api_view(['GET',])
@permission_classes((AllowAny,))
def saludo(request):
    return Response({"message": "holaa usuario de next js"})

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def saludo_private(request):
    return Response({"message": "Saludo para usuarios privados"})

@api_view(['GET',])
@permission_classes((AllowAny,))
def get_all_products(request):
    objects = Product.objects.all()
    serializer_class = ProductSerializer(objects, many=True)
    return JsonResponse({"products":serializer_class.data},safe=False,status=200)