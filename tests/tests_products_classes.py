import unittest
from classes.products import Product
from custom_exceptions.product_custom_exceptions import CustomExceptionProductMinPriceIsBiggerThanMaxPrice, \
	CustomExceptionProductHasEmptyName


class TestProductClass(unittest.TestCase):
	def test_create_product(self):
		""" Test creating a product object with valid values. ( Min price <= Max price )

		:return:
		"""
		Product(name="dummy_product", min_price=1, max_price=10)

	def test_create_product_with_wrong_min_price(self):
		""" Test creating a product object with min price <= max price

		:return:
		"""
		with self.assertRaises(CustomExceptionProductMinPriceIsBiggerThanMaxPrice):
			Product(name="dummy_product", min_price=11, max_price=10)

	def test_create_product_with_empty_name(self):
		""" Test creating a product with an empty name

		:return:
		"""
		with self.assertRaises(CustomExceptionProductHasEmptyName):
			Product(name="", min_price=1, max_price=10)


if __name__ == '__main__':
	unittest.main()
