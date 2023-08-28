from django.test import TestCase
from django.contrib.auth.models import User
from store.models import Category, Product

class TestCategoriesModel(TestCase):

	def setUp(self):
		self.data1 = Category.objects.create(name='Book', slug='Book')

	def test_category_model_entry(self):
		data = self.data1
		self.assertTrue(isinstance(data, Category))

	def test_category_model_entry(self):
		data = self.data1
		self.assertEqual(str(data), 'Book')

class TestProductsModel(TestCase):

	def setUp(self):
		Category.objects.create(name='Book', slug='Book')
		User.objects.create(username='dmitrii')
		self.data1 = Product.objects.create(category_id=1, title='Programming languages', created_by_id=1, slug='Programming languages', price=20.00)

	def test_products_model_entry(self):
		data = self.data1
		self.assertTrue(isinstance(data, Product))
		self.assertEqual(str(data), 'Programming languages')