from django.urls import path
from . import views

urlpatterns = [
    path('encrypt/', views.encrypt_view, name='encrypt'),  # Bu URL'yi kullanın
    path('decrypt/',views.decrypt_view,name='decrypt')
]
