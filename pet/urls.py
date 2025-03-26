from django.urls import path
from . import views

app_name = 'pet'

urlpatterns = [
	path('pet/<str:qr_code>/', views.PetQRView, name='pet_by_qr'),
	path('create-pet-tag/', views.CreatePetProfile, name='create_pet_tag'),

]