import logging
from typing import List
from custom_exceptions.product_custom_exceptions import CustomExceptionProductDoesNotExists, \
	CustomExceptionProductMinPriceIsBiggerThanMaxPrice, CustomExceptionProductHasEmptyName


logger = logging.getLogger(__name__)


class Product:
	""" Defines a product which can be traded in game"""

	def __init__(self,
				 name: str,
				 min_price: int,
				 max_price: int):
		"""

		:param name:
		:param min_price: Min price which the item can be traded at
		:param max_price: Max price which the item can be traded at
		"""
		if min_price > max_price:
			raise CustomExceptionProductMinPriceIsBiggerThanMaxPrice(f"Product {name} is having wrong price values!"
																	 f"Minimum price should not be smaller/equals to "
																	 f"max price!")
		if name == "":
			raise CustomExceptionProductHasEmptyName("Product has an empty name! Must not have an empty name!")

		self.name: str = name
		self.min_price: int = min_price
		self.max_price: int = max_price

	def __str__(self) -> str:
		""" Will print a string representing the product details

		:return:
		"""
		return f"Product {self.name} - min price: {self.min_price} , max price: {self.max_price}"


class PlayerProductInventory:
	""" Defines a products in the player's inventory including its amount """

	def __init__(self,
				 product: Product,
				 amount: int):
		"""

		:param product:
		:param amount:
		"""
		self.product: Product = product
		self.amount: int = amount

	def __str__(self) -> str:
		""" Will print a string representing the product details in a player inventory

		:return:
		"""
		return f"Player inventory: product {self.product.name} - , amount in player inventory: {self.amount} ," \
			   f"product prices range: min {self.product.min_price} - max {self.product.max_price}"

	@property
	def product_name(self) -> str:
		""" Returns the product name

		:return: Product name (str)
		"""
		return self.product.name


class PlayersInventory:
	""" Defines the player's inventory - which will details what products player holds and in which quantity
		# TODO - add in the future a transaction history
	"""

	def __init__(self,
				 products_list_in_game: List[Product],
				 initial_amount: int = 0):
		""" Will load all products available in a game to the inventory.
		All products will start with a default 0 amount.

		"""
		self.products_inventory_list: List[PlayerProductInventory] = []
		for product in products_list_in_game:
			self.products_inventory_list.append(PlayerProductInventory(product=product,
																	   amount=initial_amount))

	def get_product_details_in_inventory(self, product_to_get_details_on: Product) -> PlayerProductInventory:
		""" Returns product details in the inventory

		:param product_to_get_details_on:
		:return: A PlayerProductInventory of the product given
		"""
		for product_inventory in self.products_inventory_list:
			if product_inventory.product_name == product_to_get_details_on.name:
				return product_inventory
		raise CustomExceptionProductDoesNotExists(f"Product {product_to_get_details_on.name} "
												  f"doesn't exist in player's inventory! ")

	def add_product_to_inventory(self, product: Product, amount_to_add: int) -> None:
		""" Adds an amount from a product to the inventory.

		:param product:
		:param amount_to_add:
		:return None
		"""
		for product_inventory in self.products_inventory_list:
			if product_inventory.product_name == product.name:
				product_inventory.amount += amount_to_add
				return None
		raise CustomExceptionProductDoesNotExists(f"Product {product.name} doesn't exist in player's inventory! ")

	def remove_product_from_inventory(self, product: Product, amount_to_remove: int) -> None:
		""" Removes an amount from a product from the inventory.

		:param product:
		:param amount_to_remove:
		:return: None
		"""
		self.add_product_to_inventory(product=product, amount_to_add=amount_to_remove * (-1))

	def check_if_amount_of_item_exists_in_inventory(self, product: Product, amount: int) -> bool:
		""" Check if there is a minimum amount of a product in the inventory

		:param product:
		:param amount: an amount of item to be checked
		:return: boolean - true if there is enough amount of the product, else false
		"""
		product_inventory_details: PlayerProductInventory = \
			self.get_product_details_in_inventory(product_to_get_details_on=product)
		if amount <= product_inventory_details.amount:
			return True
		return False

	def get_inventory_content(self) -> List[PlayerProductInventory]:
		""" Returns a list with the inventory content.

		:return: List[Product]
		"""
		return self.products_inventory_list

	def get_product_by_name(self, product_name: str) -> PlayerProductInventory:
		""" Returns a product according to it's name.

		:param product_name:
		:return: PlayerProductInventory object
		"""
		for product_inventory in self.products_inventory_list:
			if product_inventory.product_name == product_name:
				return product_inventory
		logger.error(f"Failed in searching for product with name {product_name} in the player inventory")
		raise CustomExceptionProductDoesNotExists(f"Product {product_name} doesn't exist in player's inventory! ")
