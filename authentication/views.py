from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import RegisterSerializer, LoginSerializer, SecretSerializer
from drf_yasg import openapi

register_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username for the user'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address of the user'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for the user', format=openapi.FORMAT_PASSWORD)
    },
)

login_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password', format=openapi.FORMAT_PASSWORD)
    },
)

@swagger_auto_schema(method='post', request_body=register_request_schema)
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=login_request_schema)
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post')
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@swagger_auto_schema(method='get', responses={200: SecretSerializer})
@api_view(['GET'])
def secret_view(request):
    if request.user.is_authenticated:
        serializer = SecretSerializer(data={'message': 'This is a secret message!'})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'message': 'You must be logged in to access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
