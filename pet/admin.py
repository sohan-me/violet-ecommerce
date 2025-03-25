from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(PetType)
admin.site.register(Breed)


@admin.register(PetTag)
class PetTagAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'pet_name', 'pet_type', 'breed', 'dob', 'weight', 'gender']
	list_display_links = ['id', 'pet_name', 'pet_type']
	search_fields = ['pet_name']
	list_filter = ['pet_type', 'gender']
	readonly_fields = ['qr_code', 'qr_image']
