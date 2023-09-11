import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.http import JsonResponse
from django.core.serializers import serialize


@api_view(['POST',])
@permission_classes([AllowAny, HasAPIKey])
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
@permission_classes([AllowAny, HasAPIKey])
def login_user(request):
    if request.body:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if email is None or password is None:
            return JsonResponse({"errors": {"detail": "Please enter both email and password"}}, status=400)

        user_object = User.objects.filter(email=email).first()

        if user_object is not None:
            user_name = user_object.username

            # Autenticar al usuario
            user = authenticate(username=user_name, password=password)
            if user is not None:
                login(request, user)
                data = user.groups.all()
                data_serialized = serialize("json", data)
                data_serialized = json.loads(data_serialized)

                # Generar tokens JWT
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # Devolver el token JWT en la respuesta
                return JsonResponse({"access_token": access_token, "data_group": data_serialized})
            else:
                return JsonResponse({"errors": "Invalid credentials"}, status=400)
        else:
            return JsonResponse({"errors": "User doesn't exist"}, status=400)
    else:
        return JsonResponse({"error": "No data in the request body"}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny, HasAPIKey])
def logout_user(request):
    logout(request)
    return JsonResponse({"exit": "logout success"},status=201)