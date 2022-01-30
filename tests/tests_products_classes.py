from typing import List
import unittest
from classes.products import Product, PlayerProductInventory, PlayersInventory
from custom_exceptions.product_custom_exceptions import CustomExceptionProductMinPriceIsBiggerThanMaxPrice, \
	CustomExceptionProductHasEmptyName, CustomExceptionProductDoesNotExists


class TestProductClass(unittest.TestCase):
	""" Will test Product class """
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


class TestPlayerProductInventory(unittest.TestCase):
	""" Will test PlayerProductInventory class"""
	def test_create_product_inventory_with_bad_product(self):
		""" Will create a PlayerProductInventory with bad Product """
		with self.assertRaises(CustomExceptionProductHasEmptyName):
			PlayerProductInventory(product=Product(name="",  # Bad name - name can't be 0 characters!
												   min_price=1,
												   max_price=2),
								   amount=0)


class TestPlayersInventory(unittest.TestCase):
	""" Will test PlayerProductInventory class """
	def setUp(self):
		""" Set up some objects used generally by the tests running by this class """
		self.dummy_product = Product(name="dummy_product", min_price=1, max_price=10)
		self.dummy_products_list: List[Product] = [self.dummy_product]

	def test_create_player_inventory_and_return_a_product(self):
		""" Will create a player inventory with a product and will check if the product is returned from inventory

		:return:
		"""
		player_inventory = PlayersInventory(products_list_in_game=self.dummy_products_list,
											initial_amount=10)

		returned_product_inventory: PlayerProductInventory = \
			player_inventory.get_product_details_in_inventory(self.dummy_product)
		returned_product: Product = returned_product_inventory.product
		self.assertEqual(first=returned_product, second=self.dummy_product, msg="Same product wasn't returned!")

	def test_return_product_by_name(self):
		""" Will test ability to return a product from a player inventory by its name

		:return:
		"""
		player_inventory = PlayersInventory(products_list_in_game=self.dummy_products_list,
											initial_amount=10)
		product_inventory: PlayerProductInventory = player_inventory.get_product_by_name(product_name="dummy_product")
		product: Product = product_inventory.product
		self.assertEqual(first=product, second=self.dummy_product)

	def test_check_product_add_amount(self):
		""" Will test ability to add product amount to player inventory and to return it

		:return:
		"""
		player_inventory = PlayersInventory(products_list_in_game=self.dummy_products_list,
											initial_amount=10)
		player_inventory.add_product_to_inventory(product=self.dummy_product, amount_to_add=15)
		product_amount: int = player_inventory.\
			get_product_details_in_inventory(product_to_get_details_on=self.dummy_product).amount

		self.assertEqual(first=product_amount, second=25)
		self.assertNotEqual(first=product_amount, second=10)
		self.assertNotEqual(first=product_amount, second=15)

	def test_check_product_remove_amount(self):
		""" Will test ability to get remove product amount from inventory

		:return:
		"""
		player_inventory = PlayersInventory(products_list_in_game=self.dummy_products_list,
											initial_amount=10)
		player_inventory.remove_product_from_inventory(product=self.dummy_product, amount_to_remove=5)
		product_amount: int = player_inventory.\
			get_product_details_in_inventory(product_to_get_details_on=self.dummy_product).amount

		self.assertEqual(first=product_amount, second=5)
		self.assertNotEqual(first=product_amount, second=10)
		self.assertNotEqual(first=product_amount, second=15)

	def test_check_getting_product_which_doesnt_exist(self):
		""" Will test getting product from player inventory, where this product doesn't exist

		:return:
		"""
		with self.assertRaises(CustomExceptionProductDoesNotExists):
			player_inventory = PlayersInventory(products_list_in_game=self.dummy_products_list,
												initial_amount=10)
			player_inventory.remove_product_from_inventory(product=self.dummy_product, amount_to_remove=5)

			not_real_product: Product = Product(name="dummy_product_not_exist", min_price=1, max_price=10)

			player_inventory.get_product_details_in_inventory(product_to_get_details_on=not_real_product)


if __name__ == '__main__':
	unittest.main()
