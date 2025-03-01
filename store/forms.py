from .models import Contact
from django import forms




class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = ['first_name', 'last_name', 'email', 'subject', 'message']

	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)

		self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
		self.fields['email'].widget.attrs['placeholder'] = 'Email'
		self.fields['subject'].widget.attrs['placeholder'] = 'Subject'
		self.fields['message'].widget.attrs['placeholder'] = 'Message'

		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'