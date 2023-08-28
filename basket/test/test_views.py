from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Product, Category


class TestBasketView(TestCase):
	def setUp(self):
		User.objects.create(username='dmitrii')
		Category.objects.create(name='Books', slug='books')
		Product.objects.create(category_id=1, title='Ruby', created_by_id=1, slug='ruby', price=50.00)
		Product.objects.create(category_id=1, title='Ruby1', created_by_id=1, slug='ruby1', price=50.00)
		Product.objects.create(category_id=1, title='Ruby2', created_by_id=1, slug='ruby2', price=50.00)

		self.client.post(
				reverse('basket:basket_add'), {"productid":1, "productqty":1, "action":"post"}, xhr=True 
			)
		self.client.post(
				reverse('basket:basket_add'), {"productid":2, "productqty":2, "action":"post"}, xhr=True
			)

	def test_basket_url(self):
		response = self.client.get(reverse('basket:basket_summary'))
		self.assertEqual(response.status_code, 200)

	def test_basket_add(self):
		response = self.client.post(
				reverse('basket:basket_add'), {"productid":3, "productqty":1, "action":"post"}, xhr=True 
			)
		self.assertEqual(response.json(), {"qty":4})
		response = self.client.post(
				reverse('basket:basket_add'), {"productid":2, "productqty":1, "action":"post"}, xhr=True 
			)
		self.assertEqual(response.json(), {"qty":3})

	def test_basket_delete(self):
		response = self.client.post(
				reverse('basket:basket_delete'), {"productid":2, "action":"post"}, xhr=True 
			)
		self.assertEqual(response.json(), {"qty":1, "subtotal":"50.00"})















