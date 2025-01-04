import base64
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from enc.utils import PaillierHE
from .models import Enc
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Define OpenAPI schema for the input and output
encrypt_and_save_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'sequence': openapi.Schema(type=openapi.TYPE_STRING, description="DNA sequence to encrypt"),
        'length': openapi.Schema(type=openapi.TYPE_INTEGER, description="Length of the DNA sequence"),
        'gc_content': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="GC content percentage"),
        'gene_name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the gene", nullable=True),
        'gene_description': openapi.Schema(type=openapi.TYPE_STRING, description="Description of the gene", nullable=True),
    },
    required=['sequence', 'length'],
)

encrypt_and_save_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, description="Response message"),
        'data': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the saved record"),
                'sequence': openapi.Schema(type=openapi.TYPE_STRING, description="Original DNA sequence"),
                'encrypted_sequence': openapi.Schema(type=openapi.TYPE_STRING, description="Encrypted DNA sequence"),
                'length': openapi.Schema(type=openapi.TYPE_INTEGER, description="Length of the DNA sequence"),
                'gc_content': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="GC content percentage"),
                'gene_name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the gene"),
                'gene_description': openapi.Schema(type=openapi.TYPE_STRING, description="Description of the gene"),
            },
        ),
    },
)

@swagger_auto_schema(
    method='post',
    operation_summary="Encrypt and save DNA sequence",
    operation_description="Encrypt a DNA sequence using Paillier encryption and save it to the database.",
    request_body=encrypt_and_save_request_schema,
    responses={
        201: encrypt_and_save_response_schema,
        400: openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
        }),
        500: openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
        }),
    },
)
@csrf_exempt
@api_view(['POST'])
def encrypt_and_save(request):
    try:
        # Parse input data
        data = request.data
        sequence = data.get('sequence')
        length = data.get('length')
        gc_content = data.get('gc_content')
        gene_name = data.get('gene_name')
        gene_description = data.get('gene_description')

        # Initialize PaillierHE for encryption
        paillier = PaillierHE()

        # Encrypt the sequence
        encrypted_sequence = paillier.encrypt(int(sequence))

        # Save to database
        enc_instance = Enc.objects.create(
            sequence=sequence,
            encrypted_sequence=encrypted_sequence,
            length=length,
            gc_content=gc_content,
            gene_name=gene_name,
            gen_description=gene_description
        )

        return JsonResponse(
            {
                'message': 'Data encrypted and saved successfully.',
                'data': {
                    'id': enc_instance.id,
                    'sequence': sequence,
                    'encrypted_sequence': encrypted_sequence,
                    'length': length,
                    'gc_content': gc_content,
                    'gene_name': gene_name,
                    'gene_description': gene_description,
                }
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
