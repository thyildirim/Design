from django.urls import path
from enc import views

urlpatterns = [
    path('homo_sifre/', views.homo_encrypt, name=''),
    path('save_encrypted_data/', views.save_encrypted_data, name='save_encrypted_data'),
    path('decrypt_data/', views.decrypt_data, name='decrypt_data'),

]
