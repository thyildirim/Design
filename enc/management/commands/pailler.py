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
            '--number',
            type=float,
            required=False,
            help='The number to encrypt (required for encryption)',
        )

    def handle(self, *args, **options):
        number = options.get('number')

        he = PaillierHE()

        if number is None:
            self.stdout.write(self.style.ERROR("You must provide a number to encrypt."))
            return
        encrypted_value = he.encrypt(number)
        self.stdout.write(self.style.SUCCESS(f"Encrypted Value: {encrypted_value}"))

        try:
            decrypted_value = he.decrypt(encrypted_value)
            self.stdout.write(self.style.SUCCESS(f"Decrypted Value: {decrypted_value}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to decrypt: {e}"))
