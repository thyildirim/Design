from django.db import models

class Enc(models.Model):
    sequence = models.CharField(max_length=1000, unique=True)
    encrypted_sequence = models.CharField(null=True, blank=True)
    gene_name = models.CharField(max_length=255, null=True, blank=True)
    gen_description= models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
