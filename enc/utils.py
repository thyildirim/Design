import base64
import json
from phe import paillier, EncryptedNumber
#python manage.py pailler --number 42
class PaillierHE:
    def __init__(self):
        # self.public_key, self.private_key = paillier.generate_paillier_keypair()
        with open('./enc/pailler_public_key.json', 'r') as f:
            public_key_str = f.read()
        with open('./enc/pailler_private_key.json', 'r') as f:
            private_key_str = f.read()
        self.import_keys(public_key_str, private_key_str)

    def encrypt(self, number: int) -> str:
        encrypted: EncryptedNumber = self.public_key.encrypt(number)
        ciphertext: int = encrypted.ciphertext()
        byte_length = (ciphertext.bit_length() + 7) // 8
        ciphertext_bytes: bytes = ciphertext.to_bytes(byte_length, byteorder='big')
        encrypted_str:str = base64.b64encode(ciphertext_bytes).decode('utf-8')
        return encrypted_str

    def decrypt(self, encrypted_str: str) -> int:
        encrypted_bytes: bytes = base64.b64decode(encrypted_str)
        encrypted_int: int = int.from_bytes(encrypted_bytes, byteorder='big')
        encrypted: EncryptedNumber = EncryptedNumber(self.public_key, encrypted_int)
        decrypted_number: int = self.private_key.decrypt(encrypted)
        return decrypted_number

    def export_keys(self):
        public_key_str = json.dumps({
            'n': self.public_key.n
        })
        private_key_str = json.dumps({
            'p': self.private_key.p,
            'q': self.private_key.q,
            'public_key_n': self.public_key.n
        })
        return public_key_str, private_key_str

    def import_keys(self, public_key_str, private_key_str):
        public_key_data = json.loads(public_key_str)
        self.public_key = paillier.PaillierPublicKey(n=int(public_key_data['n']))

        private_key_data = json.loads(private_key_str)
        self.private_key = paillier.PaillierPrivateKey(
            paillier.PaillierPublicKey(n=int(private_key_data['public_key_n'])),
            int(private_key_data['p']),
            int(private_key_data['q'])
        )

    def number_to_dna(number):
        # Sayıları DNA bazlarına dönüştür
        mapping = {'1': 'A', '2': 'T', '3': 'G', '4': 'C'}
        number_string = str(number)
        dna_sequence = ''.join(mapping[digit] for digit in number_string)
        return dna_sequence

