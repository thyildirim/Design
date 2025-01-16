from django.urls import path
from . import views

urlpatterns = [
    path('encrypt/', views.RSAEncryption.encrypt_view, name='encrypt_view'),
    path('save-encrypted-dna/', views.RSAEncryption.save_encrypted_dna, name='save_encrypted_dna'),
]