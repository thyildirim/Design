from django.db import models

class EncryptedDNA(models.Model):
    name = models.CharField(max_length=100)
    encrypted_dna = models.TextField()

    def __str__(self):
        return f"Encrypted DNA {self.id}"
