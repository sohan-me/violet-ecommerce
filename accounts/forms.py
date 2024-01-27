from .models import Account, UserProfile
from django import forms




class RegistrationForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))

	class Meta:
		model = Account
		fields = ['first_name','last_name','username', 'email', 'password']



	def clean(self):	
		cleaned_data = super(RegistrationForm, self).clean()
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')

		if password != confirm_password:
			raise forms.ValidationError('Password does not match!')
		
		username = cleaned_data.get('username')
		try:
			flag = Account.objects.get(username=username).exists()
			if flag:
				raise forms.ValidationError('Username already used.')
		except:
			pass

			

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)

		self.fields['first_name'].widget.attrs['placeholder']='First Name'
		self.fields['last_name'].widget.attrs['placeholder']='Last Name'
		self.fields['username'].widget.attrs['placeholder']='username'
		self.fields['email'].widget.attrs['placeholder']='email'
		

		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'

class UserForm(forms.ModelForm):

	class Meta:

		model = Account
		fields = ['first_name', 'last_name']

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class']= 'form-control'

class UserProfileForm(forms.ModelForm):
	
	profile_image = forms.ImageField(required=False, error_messages={'Invalid':('Image Files Only.')}, widget=forms.FileInput)
	class Meta:
		
		model = UserProfile
		fields = ['phone', 'address_line', 'profile_image', 'city', 'state', 'country']

	def __init__(self, *args, **kwargs):
		super(UserProfileForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class']= 'form-control'