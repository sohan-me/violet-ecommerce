from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import PetTag, PetType, Breed
from .forms import PetInfoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
# Create your views here.

def PetQRView(request, qr_code):
	pet = get_object_or_404(PetTag, qr_code=qr_code)
	owner_profile = get_object_or_404(UserProfile, user=pet.user)

	context = {
		'pet':pet,
		'owner':pet.user,
		'owner_profile':owner_profile
	}
	return render(request, 'pet/whitelevel.html', context)



@login_required(login_url='accounts:login')
def UpdatePetProfile(request, id=None):
	pet_types = PetType.objects.all()
	breeds = Breed.objects.all()
	pet_object = get_object_or_404(PetTag, id=id, user=request.user)

	form = PetInfoForm(instance=pet_object)
	if request.method == 'POST':
		form = PetInfoForm(request.POST, request.FILES, instance=pet_object)
		if form.is_valid():
			form.save()
			messages.success(request, 'Pet profile has been updated successfully.')
			return redirect('store:Home')

		else:
			for field, errors in form.errors.items():
		 		for error in errors:
		 			messages.error(request, f"{field}: {error}")
			return redirect('pet:update_pet_tag')


	context = {
		'pet_types':pet_types,
		'breeds':breeds,
		'form':form,
		'pet':pet_object
	}

	return render(request, 'pet/pet_form.html', context)