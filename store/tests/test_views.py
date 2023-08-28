from unittest import skip
from django.http import HttpRequest

from django.test import TestCase, Client, RequestFactory

from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Category, Product

from store.views import product_all


@skip('demostrating skipping')
class TestSkip(TestCase):
	def test_skipping_example(self):
		pass

class TestViewResponses(TestCase):
	def setUp(self):
		self.c = Client()
		self.factory = RequestFactory()
		Category.objects.create(name='Books', slug='books')
		User.objects.create(username='dmitrii')
		self.data1 = Product.objects.create(category_id=1, title='Ruby', created_by_id=1, slug='ruby', price=50.00)

	def test_homepage_url(self):
		#Test allowed hosts
		response = self.c.get('/')
		self.assertEqual(response.status_code, 200)

	def test_product_detail_url(self):
		#Test Product response status
		response = self.c.get(reverse('store:product_detail', args=['ruby']))
		self.assertEqual(response.status_code, 200)

	def test_category_detail_url(self):
		#Test Category response status
		response = self.c.get(reverse('store:category_list', args=['books']))
		self.assertEqual(response.status_code, 200)

	def test_homepage_html(self):
		request = HttpRequest()
		response = product_all(request)
		html = response.content.decode('utf8')
		print(html)
		self.assertIn('<title>Home</title>', html)
		self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
		self.assertEqual(response.status_code, 200)

	def test_view_function(self):
		request = self.factory.get('/ruby')
		response = product_all(request)
		html = response.content.decode('utf8')
		self.assertIn('<title>Home</title>', html)
		self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
		self.assertEqual(response.status_code, 200)

	def test_url_allowed_hosts(self):
		#Test allowed hosts
		response = self.c.get('/', HTTP_HOST='noaddress.com')
		self.assertEqual(response.status_code, 400)
		response = self.c.get('/', HTTP_HOST='yourdomain.com')
		self.assertEqual(response.status_code, 200)















