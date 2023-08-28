from decimal import *
from store.models import Product 
from django.conf import settings
from checkout.models import DeliveryOptions


class Basket():
	def __init__(self, request):
		self.session = request.session
		basket = self.session.get(settings.BASKET_SESSION_ID)
		if settings.BASKET_SESSION_ID not in request.session:
			self.session[settings.BASKET_SESSION_ID] = {}
			basket = self.session[settings.BASKET_SESSION_ID]
		self.basket = basket

	def add(self, product, qty):
		product_id = product.id

		if product_id in self.basket:
			self.basket[product_id]['qty'] = qty
		else:
			self.basket[product_id] = {'price':str(product.regular_price), 'qty':int(qty)}
		self.save_session()

	def delete(self, product):
		#Delete product from session data
		product_id = str(product)
		print(type(product_id))
		if product_id in self.basket:
			del self.basket[product_id]
			self.save_session()

	def update(self, product, qty):
		#Update product from the session data
		product_id = str(product)

		if product_id in self.basket:
			self.basket[product_id]['qty'] = qty
		self.save_session()

	def clear(self):
		#Remove basket from the session
		del self.session[settings.BASKET_SESSION_ID]
		self.save_session()

	def save_session(self):
		self.session.modified = True

	def __iter__(self):
		product_ids = self.basket.keys()
		products = Product.objects.filter(id__in=product_ids)
		basket = self.basket.copy()

		for product in products:
			basket[str(product.id)]['product'] = product

		for item in basket.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['qty']
			yield item 

	def get_total_price(self):
		new_price = Decimal('0.00')
		subtotal = sum(Decimal(item['price'])*item['qty'] for item in self.basket.values())
		if "delivery" in self.session:
			new_price = DeliveryOptions.objects.get(id=self.session['delivery']['delivery_id']).delivery_price
		total_price = Decimal(subtotal) + Decimal(new_price)
		return total_price

	def get_subtotal_price(self):
		subtotal = sum(Decimal(item['price'])*item['qty'] for item in self.basket.values())
		return subtotal

	def get_delivery_price(self):
		delivery_price = Decimal('0.00')
		if "delivery" in self.session:
			delivery_price = DeliveryOptions.objects.get(id=self.session['delivery']['delivery_id']).delivery_price
		return delivery_price

	def __len__(self):
		#Get the basket data and count the qty of items
		return sum(item['qty'] for item in self.basket.values())

	def basket_update_delivery(self, deliveryprice=0):
		subtotal = sum(Decimal(item['price'])*item['qty'] for item in self.basket.values())
		total_price = subtotal + Decimal(deliveryprice)
		return total_price

		