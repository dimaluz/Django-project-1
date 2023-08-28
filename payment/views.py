from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from basket.basket import Basket
from order.views import payment_confirmation
import os
import stripe
import json




@login_required
def BasketView(request):
	basket = Basket(request)
	total_price = str(basket.get_total_price())
	total_price = total_price.replace('.', '')
	total_price = int(total_price)

	stripe.api_key = settings.STRIPE_SECRET_KEY
	intent = stripe.PaymentIntent.create(amount=total_price, currency='usd', metadata={'userid':request.user.id})

	context = {'client_secret':intent.client_secret, 'STRIPE_PUBLISHABLE_KEY':os.environ.get('STRIPE_PUBLISHABLE_KEY')}

	return render(request, 'payment/payment_form.html', context)


@csrf_exempt
def stripe_webhook(request):
	payload = request.body
	event = None

	try:
		event = stripe.Event.constract_from(json.loads(payload), stripe.api_key)
	except ValueError as e:
		print(e)
		return HttpResponse(status=400)

	if event.type == 'payment_intent.succeeded':
		payment_confirmation(event.data.object.client_secret)
	else:
		print('Unhandled event type: {}'.format(event.type))

	return HttpResponse(status=200)


def order_placed(request):
	basket = Basket(request)
	basket.clear()
	return render(request, 'payment/orderplaced.html')


















