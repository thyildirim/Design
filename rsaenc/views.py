import base64
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from django.http import JsonResponse

from rsaenc.models import EncryptedDNA

class RSAEncryption:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        """Generates a new RSA key pair and stores them as Base64 encoded strings."""
        key = RSA.generate(2048)
        self.private_key = base64.b64encode(key.export_key()).decode('utf-8')
        self.public_key = base64.b64encode(key.publickey().export_key()).decode('utf-8')

    def import_keys(self, private_key=None, public_key=None):
        """Imports Base64 encoded RSA keys."""
        if private_key:
            self.private_key = private_key
        if public_key:
            self.public_key = public_key

    def encrypt_view(request):
       if request.method == 'POST':
           try:
               data = json.loads(request.body)
               sequence = data.get('sequence', '')
               rsa = RSAEncryption()
               rsa.generate_keys()  
               encrypted_sequence = rsa.encrypt_message(sequence)
               return JsonResponse({'encrypted_data': encrypted_sequence})
           except Exception as e:
               return JsonResponse({'error': str(e)}, status=400)
       return JsonResponse({'error': 'Invalid request method'}, status=405)



    def encrypt_message(self, message):
        """Encrypts a message using the public key."""
        if not self.public_key:
            raise ValueError("Public key is not set.")
        public_key = RSA.import_key(base64.b64decode(self.public_key))
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_message = cipher.encrypt(message.encode('utf-8'))
        # Encode the encrypted message in Base64
        return base64.b64encode(encrypted_message).decode('utf-8')

    def save_encrypted_dna(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                sequence = data.get('sequence', '')
                rsa = RSAEncryption()
                rsa.generate_keys()  # Ensure keys are generated or imported
                encrypted_sequence = rsa.encrypt_message(sequence)
                
                # Save to database
                EncryptedDNA.objects.create(
                    sequence=sequence,
                    encrypted_sequence=encrypted_sequence
                )
                
                return JsonResponse({'message': 'Data saved successfully'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    def decrypt_message(self, encrypted_message_base64):
        """Decrypts a message using the private key."""
        if not self.private_key:
            raise ValueError("Private key is not set.")
        private_key = RSA.import_key(base64.b64decode(self.private_key))
        cipher = PKCS1_OAEP.new(private_key)
        # Decode the Base64 encrypted message back to bytes
        encrypted_message = base64.b64decode(encrypted_message_base64)
        decrypted_message = cipher.decrypt(encrypted_message).decode('utf-8')
        return decrypted_message

if __name__ == "__main__":
    rsa = RSAEncryption()

    # Generate a new key pair
    rsa.generate_keys()
    print("Generated Public Key (Base64):")
    print(rsa.public_key)
    print("Generated Private Key (Base64):")
    print(rsa.private_key)

    # Encrypt and decrypt a message
    message = "This is a secret message"
    encrypted_message_base64 = rsa.encrypt_message(message)
    print(f"Encrypted (Base64): {encrypted_message_base64}")

    decrypted_message = rsa.decrypt_message(encrypted_message_base64)
    print(f"Decrypted: {decrypted_message}")

    # Example of importing Base64 keys
    rsa.import_keys(private_key=rsa.private_key, public_key=rsa.public_key)
    encrypted_message_base64 = rsa.encrypt_message(message)
    decrypted_message = rsa.decrypt_message(encrypted_message_base64)
    print(f"Decrypted with imported Base64 keys: {decrypted_message}")
