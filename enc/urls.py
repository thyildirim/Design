from django.urls import path
from .views import encrypt_and_save

urlpatterns = [
    path('encrypt-and-save/', encrypt_and_save, name='encrypt_and_save'),
]
