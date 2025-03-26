from django.urls import path
from . import views

app_name = 'pet'

urlpatterns = [
	path('pet/<str:qr_code>/', views.PetQRView, name='pet_by_qr'),
	path('update-pet-tag/<int:id>/', views.UpdatePetProfile, name='update_pet_tag'),

]