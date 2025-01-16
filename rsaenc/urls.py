from django.urls import path
from . import views

urlpatterns = [
    path('encrypt/', views.RSAEncryption.encrypt_view, name='encrypt_view'),
    path('save-encrypted-dna/', views.RSAEncryption.save_encrypted_dna, name='save_encrypted_dna'),
    path('decrypt/', views.RSAEncryption.decrypt_message, name='decrypt_message_view'),
    path('decrypt-dna/', views.RSAEncryption.decrypt_message_view, name='decrypt_dna_view'),
]