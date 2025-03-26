from django import forms
from .models import PetTag


class PetInfoForm(forms.ModelForm):
	class Meta:
		model = PetTag
		exclude = ['user', 'qr_code', 'qr_image']

