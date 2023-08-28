from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages

from .models import DeliveryOptions
from basket.basket import Basket
from account.models import Address

@login_required
def deliverychoices(request):
	deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
	context = {'deliveryoptions':deliveryoptions}
	return render(request, 'store/checkout/delivery_choices.html', context)

@login_required
def basket_update_delivery(request):
	basket = Basket(request)
	if request.POST.get("action") == "post":
		delivery_option = int(request.POST.get('deliveryoption'))
		delivery_type = DeliveryOptions.objects.get(id=delivery_option)
		updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)

		session = request.session
		if 'delivery' not in request.session:
			session['delivery'] = {
				'delivery_id': delivery_type.id, 
			}
		else:
			session['delivery']['delivery_id'] = delivery_type.id
			session.modified = True
		
		response = JsonResponse({'total_price': updated_total_price, 'delivery_price': delivery_type.delivery_price})
		return response

@login_required      
def delivery_address(request):
	session = request.session
	if "delivery" not in request.session:
		messages.success(request, "Please select the delivery option")
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	addresses = Address.objects.filter(customer=request.user).order_by("-default")
	if "address" not in request.session:
		session["address"] = {"address_id":str(addresses[0].id)}
	else:
		session["address"]["address_id"] = str(addresses[0].id)
		session.modified = True
	context = {'addresses':addresses}
	return render(request, 'store/checkout/delivery_address.html', context)

@login_required
def payment_selection(request):
	if "address" not in request.session:
		messages.success(request, "Please select address option")
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	context = {}
	return render(request, 'store/checkout/payment_selection.html', context)

def payment_successful(request):
	pass
