from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import PetTag
from .forms import PetInfoForm
# Create your views here.

def PetQRView(request, qr_code):
	pet = get_object_or_404(PetTag, qr_code=qr_code)

	context = {
		'pet':pet,
		'owner':pet.user,
	}

	return HttpResponse(f'{pet.pet_name} -- {pet.pet_type} !')



def CreatePetProfile(request):
	return render(request, 'pet/pet_form.html')