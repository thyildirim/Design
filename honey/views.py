from django.shortcuts import render
from django.http import JsonResponse
import base64
import random
import json

from honey.models import Honey

# ACGT harf kümesi
DNA_CHARSET = "ACGT"

def generate_fake_dna_sequence(length: int) -> str:
    """Yanlış cevap için rastgele ACGT dizisi oluştur."""
    return ''.join(random.choice(DNA_CHARSET) for _ in range(length))

def honey_encrypt(dna_sequence: str, key: str) -> str:
    """DNA dizisini Base64 ile şifrele ve anahtarı da dahil et."""
    combined_sequence = dna_sequence + key
    byte_data = combined_sequence.encode('utf-8')
    encrypted_data = base64.b64encode(byte_data).decode('utf-8')
    return encrypted_data

from honey.models import Honey  # Honey modelini içe aktar

def honey_decrypt(encrypted_data: str, key: str) -> str:
    """Honey Encryption ile şifre çöz."""
    try:
        # Veritabanında şifrelenmiş veri ve anahtar ile eşleşen bir kayıt arayın
        record = Honey.objects.filter(encrypted_sequence=encrypted_data, key=key).first()
        
        if record:
            # Eşleşen bir kayıt bulunduysa, orijinal DNA dizisini döndür
            return record.sequence
        else:
            # Eşleşen kayıt bulunamazsa, sahte bir DNA dizisi döndür
            return generate_fake_dna_sequence(len(encrypted_data))
    except Exception as e:
        # Hata durumunda (örneğin veritabanı erişim hatası) sahte bir veri döndür
        return generate_fake_dna_sequence(len(encrypted_data))

def decrypt_view(request):
    if request.method == 'POST':
        try:
            # JSON verisini al
            data = json.loads(request.body)
            encrypted_data = data.get('encrypted_data')
            key = data.get('key')

            if not encrypted_data or not key:
                return JsonResponse({'success': False, 'message': 'Şifreli veri ve anahtar (key) boş olamaz'}, status=400)

            # Veritabanında eşleşen bir kayıt arayın
            record = Honey.objects.filter(encrypted_sequence=encrypted_data, key=key).first()

            if record:
                # Kayıt bulunduysa, orijinal DNA dizisini döndür
                decrypted_data = record.sequence
                return JsonResponse({'success': True, 'decrypted_data': decrypted_data})
            else:
                # Kayıt bulunamazsa, sahte bir DNA dizisi oluştur
                fake_data = generate_fake_dna_sequence(len(encrypted_data))
                return JsonResponse({'success': True, 'decrypted_data': fake_data})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Geçersiz JSON formatı'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Sadece POST metodu destekleniyor.'}, status=405)



def encrypt_view(request):
    if request.method == 'POST':
        try:
            # JSON verisini al
            data = json.loads(request.body)

            sequence = data['sequence']
            key = data['key']
            gene_name = data['gene_name']
            gen_description = data['gen_description']
            correct_key = key  # Şifreleme anahtarı doğrulama için aynı olacak

            # Şifreleme
            encrypted_data = honey_encrypt(sequence, key)

            # Şifre çözme işlemi
            decrypted_data = honey_decrypt(encrypted_data, key)

            # Veritabanına kaydetme işlemi
            dna_record = Honey(
                gene_name=gene_name,
                sequence=sequence,
                gen_description=gen_description,
                encrypted_sequence=encrypted_data,
                key=key
            )
            dna_record.save()

            return JsonResponse({
                'decrypted_data': decrypted_data,
                'message': 'Data saved successfully'
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

    return render(request, 'index.html')
