from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .forms import RegistrationForm, UserEditForm, UserAddressForm
from .token import account_activation_token
from .models import Customer, Address
from order.views import user_orders

from store.models import Product

from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required
def wishlist(request):
	products = Product.objects.filter(users_wishlist=request.user)
	context = {'wishlist':products}
	return render(request, 'store/account/dashboard/user_wish_list.html', context)

@login_required
def add_to_wishlist(request, id):
	product = get_object_or_404(Product, id=id)
	if product.users_wishlist.filter(id=request.user.id).exists():
		product.users_wishlist.remove(request.user)
		messages.success(request, product.title+" has been removed from your WishList")
	else:
		product.users_wishlist.add(request.user)
		messages.success(request, product.title+" has been added to your WishList")
	return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def dashboard(request):
	orders = user_orders(request)
	contex = {'orders':orders}
	return render(request, 'store/account/dashboard/dashboard.html', contex)


@login_required
def edit_details(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user, data=request.POST)
		if user_form.is_valid():
			user_form.save()
	else:
		user_form = UserEditForm(instance=request.user)
	return render(request, 'store/account/dashboard/edit_details.html', {'user_form':user_form})

@login_required
def delete_user(request):
	user = Customer.objects.get(user_name=request.user)
	user.is_active = False
	user.save()
	logout(request)
	return redirect('account:delete_confirmation')



def account_register(request):
	#if request.user.is_authenticated:
		#return redirect('/')

	if request.method == 'POST':
		registerForm = RegistrationForm(request.POST)
		if registerForm.is_valid():
			user = registerForm.save(commit=False)
			user.email = registerForm.cleaned_data['email']
			user.set_password(registerForm.cleaned_data['password'])
			user.is_active = False
			user.save()
			#Setup email
			current_site = get_current_site(request)
			subject = 'Account activation'
			message = render_to_string('store/account/registration/account_activation_email.html', 
				{'user':user, 
				'domain':current_site.domain, 
				'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
				'token':account_activation_token.make_token(user), 
				})
			user.email_user(subject=subject, message=message)
			return render(request, 'store/account/registration/register_email_confirm.html', {'form':registerForm})
	else:
		registerForm = RegistrationForm()
		
	return render(request, 'store/account/registration/register.html', {'form':registerForm})


def account_activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = Customer.objects.get(pk=uid)
	except:
		pass
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		return redirect('account:dashboard')
	else:
		return render(request, 'store/account/registration/activation_invalid.html')
	

#Update, Delete and Add Addresses
@login_required
def view_address(request):
	addresses = Address.objects.filter(customer=request.user)
	context = {'addresses':addresses}
	return render(request, 'store/account/dashboard/addresses.html', context)

@login_required
def add_address(request):
	if request.method == 'POST':
		address_form = UserAddressForm(data=request.POST)
		if address_form.is_valid():
			address_form = address_form.save(commit=False)
			address_form.customer = request.user
			address_form.save()
			return HttpResponseRedirect(reverse('account:addresses'))
	else:
		address_form = UserAddressForm()
	context = {'form':address_form}
	return render(request, 'store/account/dashboard/edit_addresses.html', context)

@login_required
def edit_address(request, id):
	if request.method == 'POST':
		address = Address.objects.get(pk=id, customer=request.user)
		address_form = UserAddressForm(instance=address, data=request.POST)
		if address_form.is_valid():
			address_form.save()
			return HttpResponseRedirect(reverse('account:addresses'))
	else:
		address = Address.objects.get(pk=id, customer=request.user)
		address_form = UserAddressForm(instance=address)
	context = {'form':address_form}
	return render(request, 'store/account/dashboard/edit_addresses.html', context)

@login_required
def delete_address(request, id):
	address = Address.objects.filter(pk=id, customer=request.user).delete()
	return redirect('account:addresses')

@login_required
def set_default(request, id):
	Address.objects.filter(customer=request.user, default=True).update(default=False)
	Address.objects.filter(pk=id, customer=request.user).update(default=True)
	previous_url = request.META.get("HTTP_REFERER")
	if "delivery_address" in previous_url:
		return redirect("checkout:delivery_address")
	return redirect('account:addresses')





































