from django.urls import path
from rsaenc import views
urlpatterns = [
    path('encrypt/', views.encrypt_dna_view, name='dna_list'),



]
