from typing import List


class Product:
	""" Defines a product which can be traded """

	def __init__(self, name: str, min_price: int, max_price: int):
		"""

		:param name:
		:param min_price: Min price which the item can be traded at
		:param max_price: Max price which the item can be traded at
		"""
		self.name: str = name
		self.min_price: int = min_price
		self.max_price: int = max_price


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

	@property
	def product_name(self) -> str:
		""" Returns the product name

		:return: Product name
		"""
		return self.product.name


class PlayersInventory:
	""" Defines the player's inventory - what products he hold and in which quantity
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

	def get_product_details_in_inventory(self, product_to_get_details_on: Product):
		""" Returns product details in the inventory"""
		for product_inventory in self.products_inventory_list:
			if product_inventory.product_name == product_to_get_details_on.name:
				return product_inventory

	def add_product_to_inventory(self, product: Product, amount_to_add: int) -> None:
		""" Adds an amount from a product to the inventory.

		:return None
		"""
		for product_inventory in self.products_inventory_list:
			if product_inventory.product_name == product.name:
				product_inventory.amount += amount_to_add

	def remove_product_from_inventory(self, product: Product, amount_to_remove: int) -> None:
		""" Removes an amount from a product from the inventory.

		:return: None
		"""
		self.add_product_to_inventory(product=product, amount_to_add=amount_to_remove * (-1))

	def get_inventory_content(self) -> List[PlayerProductInventory]:
		""" Returns a list with the inventory content.

		:return: List[Product]
		"""
		return self.products_inventory_list

	def get_product_by_name(self, product_name) -> PlayerProductInventory:
		""" Returns a product according to it's name.

		:return: PlayerProductInventory object """
		# TODO - add exception in case wrong name was given!
		for product_inventory in self.products_inventory_list:
			if product_inventory.product_name == product_name:
				return product_inventory
