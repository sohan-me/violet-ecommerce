from django.db import models
from accounts.models import Account
import uuid, qrcode
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from urllib.parse import urljoin
from django.core.exceptions import ValidationError
from io import BytesIO
from django.core.files import File
from django.urls import reverse
# Create your models here.

class PetType(models.Model):
	type = models.CharField(max_length=200)

	def __str__(self):
		return self.type


class Breed(models.Model):
	breed = models.CharField(max_length=200)

	def __str__(self):
		return self.breed


class PetTag(models.Model):

	GENDER = (
		('Male', 'Male'),
		('Female', 'Female'),
		('Unknown', 'Unknown'),
	)
	

	user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='pets')
	pet_name = models.CharField(max_length=255)
	pet_type = models.ForeignKey(PetType, on_delete=models.SET_NULL, null=True, blank=True)
	breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True, blank=True)
	image = models.ImageField(upload_to='pets/', null=True, blank=True)
	age = models.CharField(max_length=5, null=True, blank=True)
	weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	gender = models.CharField(choices=GENDER, max_length=20, null=True, blank=True)
	additional_note = models.TextField(null=True, blank=True)
	qr_code = models.CharField(max_length=30, unique=True, blank=True, null=True)
	qr_image = models.ImageField(upload_to='pets/qrcodes/', null=True, blank=True)


	def get_absolute_url(self):
		return reverse('pet:pet_by_qr', kwargs={'qr_code': self.qr_code})

	def get_full_qr_url(self):
		return urljoin(settings.BASE_URL, self.get_absolute_url())

	def clean(self):
		if not self.qr_code:
			self.qr_code = f'{self.pet_name.upper()}-{uuid.uuid4().hex[:8].upper()}'

	def __str__(self):
		return self.pet_name


@receiver(post_save, sender=PetTag)
def assign_qr_code(sender, instance, created, **kwargs):
	if not instance.qr_code:
		instance.qr_code = f'{instance.pet_name.upper()}-{uuid.uuid4().hex[:8].upper()}'
		instance.save()

	if created or not instance.qr_image:
		generate_qr_code_image(instance)



def generate_qr_code_image(pet_profile):
    """
    Generates and saves QR code image for the pet profile
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    url = pet_profile.get_full_qr_url()
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    file_name = f"pet_qr_{pet_profile.qr_code}.png"
    
    if pet_profile.qr_image:
        # Delete old file if exists
        pet_profile.qr_image.delete(save=False)
    
    pet_profile.qr_image.save(file_name, File(buffer), save=False)
    pet_profile.save()