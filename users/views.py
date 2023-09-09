import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.core.serializers import serialize

# Create your views here.
@api_view(['POST',])
@permission_classes((AllowAny,))
def create_user_client( request ):
    if ( request.body ):

        if Group.objects.get(name="cliente"):
            grupo_cliente = Group.objects.get(name="cliente")
        else:
            grupo_cliente = Group(name="cliente")
            grupo_cliente.save()
        
        data = json.loads(request.body)

        first_name = data.get('firstname')
        last_name = data.get('lastname')
        password = data.get('password')
        email = data.get('email')

        user_object = User.objects.filter(email=email)

        if ( user_object.count() == 0):
            if ( first_name and last_name and password and email):
                username = email + "_" + first_name + "_" + last_name

                nuevo_usuario = User.objects.create(username=username, email=email)
                nuevo_usuario.set_password(password)
                nuevo_usuario.first_name = first_name
                nuevo_usuario.last_name = last_name
                nuevo_usuario.groups.add(grupo_cliente)
                nuevo_usuario.save()

                return JsonResponse({"message": "usuario creado con exito"})
            else: 
                return JsonResponse({"error": "no data complete"},status=500)
        else: 
            return JsonResponse({"error": "User already exits"},status=500)
    else:
        return JsonResponse({"error": "no data body"},status=500)

@api_view(['POST'])
@permission_classes((AllowAny,))
def login_user(request):
    if ( request.body ):
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if email is None:
            return JsonResponse({"errors": {"detail": "Please enter username"}}, status=400)
        elif password is None:
            return JsonResponse({"errors": {"detail": "Please enter password"}}, status=400)

        # user_object = User.objects.get(email=email)
        user_object = User.objects.filter(email=email)
        
        if ( user_object.count() > 0) :
            user_name = user_object[0].username

            # authentication user
            user = authenticate(username=user_name, password=password)
            if user is not None:
                login(request, user)
                data = user.groups.all()
                data_serialized = serialize("json", data)
                data_serialized = json.loads(data_serialized)

                return JsonResponse({"success": "User has been logged in", "group": data_serialized})
            return JsonResponse({"errors": "Invalid credentials"},status=400,)
        else:
            return JsonResponse({"errors": "User dont exists"},status=400,)
    else:
        return JsonResponse({"error":"no data on body"},status=500)

@api_view(['POST'])
@permission_classes((AllowAny,))
def logout_user(request):
    logout(request)
    return JsonResponse({"exit": "logout success"},status=201)