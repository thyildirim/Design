from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from enc.models import Enc
from enc.utils import PaillierHE
import json

def dna_to_number(sequence):
    # DNA dizisini sayıya çevirme
    mapping = {'A': '1', 'T': '2', 'G': '3', 'C': '4'}
    number_string = ''.join(mapping[base] for base in sequence.upper())
    return int(number_string)

@csrf_exempt
def number_to_dna(number):
    # Sayıyı DNA dizisine çevirme
    mapping = {1: 'A', 2: 'T', 3: 'G', 4: 'C'}
    number_str = str(number)
    return ''.join(mapping[int(digit)] for digit in number_str)

def homo_encrypt(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sequence = data.get('sequence')
            gene_name = data.get('gene_name', 'Unknown')

            # Geçerli DNA dizisi olup olmadığını kontrol et
            if not sequence or not all(base in 'ATGC' for base in sequence.upper()):
                return JsonResponse({'error': 'Invalid DNA sequence'}, status=400)

            # Şifreleme işlemi
            number = dna_to_number(sequence)
            he = PaillierHE()
            encrypted_value = he.encrypt(number)

            return JsonResponse({
                'encrypted': encrypted_value,
                'gene_name': gene_name,
                'original_sequence': sequence
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def save_encrypted_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            sequence = data.get('sequence')
            encrypted_sequence = data.get('encrypted_sequence')
            gene_name = data.get('gene_name')
            description = data.get('description')

            # Veritabanına kaydetme
            enc_instance = Enc(
                sequence=sequence,
                encrypted_sequence=encrypted_sequence,
                gene_name=gene_name,
                gen_description=description
            )
            enc_instance.save()

            return JsonResponse({'message': 'Data successfully saved'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def decrypt_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            encrypted_value = data.get('encrypted_value')

            # Homomorfik şifre çözme işlemi
            he = PaillierHE()
            decrypted_value = he.decrypt(encrypted_value)

            if decrypted_value is None:
                # Eğer şifre çözülemiyorsa, anlamlı bir hata mesajı döndürüyoruz
                return JsonResponse({'error': 'Şifre çözülemedi. Şifre yanlış olabilir.'}, status=400)

            # Sayıyı DNA dizisine dönüştürme
            decrypted_dna = number_to_dna(decrypted_value)

            # Çözümlenen DNA dizisini geri gönder
            return JsonResponse({
                'decrypted': decrypted_dna,
            }, status=200)

        except Exception as e:
            # Genel bir hata ile karşılaşıldığında 500 hatası döndürüyoruz
            return JsonResponse({'error': 'Internal Server Error: ' + str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
