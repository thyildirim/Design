from django.db import models

class Honey(models.Model):
    sequence = models.CharField(max_length=1000, unique=True)  # DNA dizisi
    encrypted_sequence = models.CharField(max_length=1000, null=True, blank=True)  # Şifrelenmiş DNA dizisi
    gene_name = models.CharField(max_length=255, null=True, blank=True)  # Gen ismi
    gen_description = models.TextField(null=True, blank=True)  # Gen açıklaması
    key = models.CharField(max_length=20)  # Anahtar 
    created_at = models.DateTimeField(auto_now_add=True)  # Kaydedilme zamanı
    updated_at = models.DateTimeField(auto_now=True)  # Güncellenme zamanı
