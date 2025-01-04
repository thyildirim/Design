import os
from django.core.management.base import BaseCommand
from django.conf import settings

from enc.utils import PaillierHE


class Command(BaseCommand):
    help = 'Encrypt or decrypt a number using the Paillier Homomorphic Encryption scheme'

    def add_arguments(self, parser):
        parser.add_argument(
            'operation',
            type=str,
            choices=['encrypt', 'decrypt'],
            help='Specify the operation: encrypt or decrypt',
        )
        parser.add_argument(
            '--number',
            type=float,
            required=False,
            help='The number to encrypt (required for encryption)',
        )
        parser.add_argument(
            '--encrypted',
            type=str,
            required=False,
            help='The encrypted value to decrypt (required for decryption)',
        )

    def handle(self, *args, **options):
        operation = options['operation']
        number = options.get('number')
        encrypted = options.get('encrypted')

        he = PaillierHE()

        if operation == 'encrypt':
            if number is None:
                self.stdout.write(self.style.ERROR("You must provide a number to encrypt."))
                return
            encrypted_value = he.encrypt(number)
            self.stdout.write(self.style.SUCCESS(f"Encrypted Value: {encrypted_value}"))

        elif operation == 'decrypt':
            if encrypted is None:
                self.stdout.write(self.style.ERROR("You must provide an encrypted value to decrypt."))
                return
            try:
                encrypted_number = eval(encrypted)  # Convert string to encrypted number object
                decrypted_value = he.decrypt(encrypted_number)
                self.stdout.write(self.style.SUCCESS(f"Decrypted Value: {decrypted_value}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to decrypt: {e}"))
