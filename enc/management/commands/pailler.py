from phe import EncryptedNumber
from django.core.management.base import BaseCommand
from enc.utils import PaillierHE

def dna_to_number(sequence):
    # DNA bazlarını sayılara dönüştür
    mapping = {'A': '1', 'T': '2', 'G': '3', 'C': '4'}
    number_string = ''.join(mapping[base] for base in sequence.upper())
    return int(number_string)

class Command(BaseCommand):
    help = 'Encrypt or decrypt DNA sequences using Paillier cryptosystem'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            type=str,
            choices=['encrypt', 'decrypt'],
            help='Specify the operation: encrypt or decrypt',
        )
        parser.add_argument(
            '--sequence',
            type=str,
            help='DNA sequence to encrypt/decrypt (use A, T, G, C)',
        )

    def handle(self, *args, **options):
        action = options['action']
        sequence = options.get('sequence')
        he = PaillierHE()

        if action == 'encrypt':
            if not sequence or not all(base in 'ATGC' for base in sequence.upper()):
                self.stdout.write(self.style.ERROR('Please provide a valid DNA sequence using only A, T, G, C'))
                return
            
            # DNA dizisini sayıya çevir
            number = dna_to_number(sequence)
            encrypted_value = he.encrypt(number)
            self.stdout.write(self.style.SUCCESS(f'Original DNA: {sequence}'))
            self.stdout.write(self.style.SUCCESS(f'Encrypted: {encrypted_value}'))

            try:
                decrypted_value = he.decrypt(encrypted_value)
                self.stdout.write(self.style.SUCCESS(f'Decrypted DNA: {decrypted_value}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to decrypt: {e}'))

        elif action == 'decrypt':
            if not sequence:
                self.stdout.write(self.style.ERROR('Please provide an encrypted sequence'))
                return
            
            try:
                decrypted_value = he.decrypt(sequence)
                self.stdout.write(self.style.SUCCESS(f'Decrypted DNA: {decrypted_value}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to decrypt: {e}'))
