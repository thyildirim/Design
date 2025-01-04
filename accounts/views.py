from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import RegisterSerializer, LoginSerializer
from .dto import register_request_schema, login_request_schema

@swagger_auto_schema(method='post', request_body=register_request_schema)
@api_view(['POST'])
def register(request):
    if request.method != 'POST':
        return
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        error_messages = [f"{field}: {' '.join(errors)}" for field, errors in serializer.errors.items()]
        error_message_str = "\n".join(error_messages)
        return Response({'message' : error_message_str}, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

@swagger_auto_schema(method='post', request_body=login_request_schema)
@api_view(['POST'])
def login_view(request):
    if request.method != 'POST':
        return
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=serializer.validated_data['username'],
                        password=serializer.validated_data['password'])
    if user is None:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    login(request, user)
    return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)

@swagger_auto_schema(method='post')
@api_view(['POST'])
def logout_view(request):
    if request.method != 'POST':
        return
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@swagger_auto_schema(method='get')
@api_view(['GET'])
def secret_view(request):
    if not request.user.is_authenticated:
        return Response({'message': 'You must be logged in to access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
    return Response({'message': 'This is a secret message!'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def ping(request):
    return Response({'message': 'pong'}, status=status.HTTP_200_OK)
