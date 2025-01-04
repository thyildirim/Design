import json
from phe import paillier

class PaillierHE:
    def __init__(self):
        # self.public_key, self.private_key = paillier.generate_paillier_keypair()
        with open('./enc/pailler_public_key.json', 'r') as f:
            public_key_str = f.read()
        with open('./enc/pailler_private_key.json', 'r') as f:
            private_key_str = f.read()
        self.import_keys(public_key_str, private_key_str)

    def encrypt(self, number):
        return self.public_key.encrypt(number).ciphertext(be_secure=True)

    def decrypt(self, encrypted_number):
        return self.private_key.decrypt(encrypted_number)

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
