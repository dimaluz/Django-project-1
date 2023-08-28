from django import forms
from .models import Customer, Address
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm


class UserAddressForm(forms.ModelForm):

	class Meta:
		model = Address
		fields = ['full_name', 'phone', 'address_line', 'address_line2', 'town_city', 'postcode']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['full_name'].widget.attrs.update({'class':'form-control mb-2 account-form', 'placeholder':'Full Name'})
		self.fields['phone'].widget.attrs.update({'class':'form-control mb-2 account-form', 'placeholder':'Phone'})
		self.fields['address_line'].widget.attrs.update({'class':'form-control mb-2 account-form', 'placeholder':'Address'})
		self.fields['address_line2'].widget.attrs.update({'class':'form-control mb-2 account-form', 'placeholder':'Another address'})
		self.fields['town_city'].widget.attrs.update({'class':'form-control mb-2 account-form', 'placeholder':'Location'})
		self.fields['postcode'].widget.attrs.update({'class':'form-control mb-2 account-form', 'placeholder':'Postcode'})


class UserLoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Username', 'id':'login-username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password', 'id':'login-pwd'}))


class RegistrationForm(forms.ModelForm):
	user_name = forms.CharField(label="User Name", max_length=150, min_length=4, help_text="Required")
	email = forms.EmailField(max_length=150, help_text="Required")
	password = forms.CharField(label="Password", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

	class Meta:
		model = Customer
		fields = ('user_name', 'email',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['user_name'].widget.attrs.update({'class':'form-control mb-3', 'placeholder':'Username'})
		self.fields['email'].widget.attrs.update({'class':'form-control mb-3', 'placeholder':'Email', 'name':'email'})
		self.fields['password'].widget.attrs.update({'class':'form-control mb-3', 'placeholder':'Password'})
		self.fields['password2'].widget.attrs.update({'class':'form-control', 'placeholder':'Repeat Password'})

	def clean_username(self):
		user_name = self.cleaned_data['user_name'].lower()
		user_count = Customer.objects.filter(user_name=user_name)
		if user_count.count():
			raise forms.ValidationError("User with such kind of name already exists")
		return user_name

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError("Password doesn't match")
		return cd['password2']

	def clean_email(self):
		email = self.cleaned_data['email']
		if Customer.objects.filter(email=email).exists():
			raise forms.ValidationError("Email already exists")
		return email


class UserEditForm(forms.ModelForm):

	email = forms.EmailField(label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'email', 'id':'form-email', 'readonly':'readonly'}))
	first_name = forms.CharField(label='Username', min_length=4, max_length=150, widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Firstname', 'id':'form-lastname'}))
	
	class Meta:
		model = Customer
		fields = ('email', 'first_name')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['first_name'].required = True
		self.fields['email'].required = True


class PwdResetForm(PasswordResetForm):
	email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Email', 'id':'form-email'}))

	def clean_email(self):
		email = self.cleaned_data['email']
		user = Customer.objects.get(email=email)
		if not user:
			raise forms.ValidationError('There is no any user with this email')
		return email


class PwdResetConfirmForm(SetPasswordForm):
	new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'class':'form-control mb-3', 'placeholder':'New password', 'id':'form-newpass'}))
	new_password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class':'form-control mb-3', 'placeholder':'Repeat password', 'id':'form-newpass2'}))











