from .models import Order
from django import forms




class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		exclude = ['user', 'payment', 'order_number', 'email', 'order_total', 'tax', 'status', 'is_ordered', 'created_at', 'updated_at']

	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)

		self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
		self.fields['street_address'].widget.attrs['placeholder'] = 'Street Address'
		self.fields['country'].widget.attrs['placeholder'] = 'Country'
		self.fields['city'].widget.attrs['placeholder'] = 'City'
		self.fields['postal_code'].widget.attrs['placeholder'] = 'Post Code/Zip'
		self.fields['phone'].widget.attrs['placeholder'] = 'Phone Number'

		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'