from django.core.management.base import BaseCommand

from enc.utils import PaillierHE


class Command(BaseCommand):
    help = 'Encrypt or decrypt a number using the Paillier Homomorphic Encryption scheme'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            type=float,
            required=False,
            help='The number to encrypt (required for encryption)',
        )

    def handle(self, *args, **options):
        number = int(options.get('number'))

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
