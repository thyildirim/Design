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
