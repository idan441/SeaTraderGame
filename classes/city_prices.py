from typing import List, Dict
import random
from classes.products import Product
from custom_exceptions.city_custom_exceptions import CustomExceptionCityNameNotFound
from custom_exceptions.product_custom_exceptions import CustomExceptionProductDoesNotExists


"""
Represents the prices in the different cities in the game.
The prices will be used by the player to buy or sell products.
"""


class ProductsPricesInCity:
	""" Represents the current prices in a city.
	Needed to load: Products list in the game"""
	def __init__(self, products_list: List[Product]):
		"""

		:param products_list: A list of all products in a specific Sea Trader game
		"""
		self.products_list: List[Product] = products_list
		self.products_prices: Dict[Product, int] = {}

		# Generate initial products prices
		self.generate_prices_for_the_city()

	def generate_prices_for_the_city(self) -> None:
		""" Will generate prices for all products in the city.
		Prices are changed every day - by using this function

		Each product price will be in a range as defined in the Product object representing the product.

		:return: None
		"""
		self.products_prices = {}
		for product in self.products_list:
			self.products_prices[product] = random.randint(product.min_price, product.max_price)
		return None

	def get_price_for_product(self, product: Product) -> int:
		""" Returns the price for a specific product.

		:param product: A product used in the game
		:return: int
		"""
		try:
			return self.products_prices[product]
		except KeyError:
			raise CustomExceptionProductDoesNotExists(f"Product {product.name} doesn't exist in player's inventory! ")

	def get_prices_of_all_products_as_dict(self) -> Dict[str, int]:
		""" Will return a dictionary with all products and their current price.

		:return: Dict[str, any]
		"""
		prices_dict: Dict[str, int] = {}
		for product, price in self.products_prices.items():
			prices_dict[product.name] = price
		return prices_dict


class ProductsPricesInAllCities:
	""" Manages all prices in all cities.
	Prices are changed every day in game.
	"""
	def __init__(self, cities_names_in_game: List[str], products_in_game: List[Product]):
		"""

		:param cities_names_in_game:
		:param products_in_game:
		"""
		self.cities_names: List[str] = cities_names_in_game
		self.products_list: List[Product] = products_in_game
		self.prices_in_cities: Dict[str, ProductsPricesInCity] = {}
		self.generate_prices_for_all_cities()

	def generate_prices_for_all_cities(self) -> None:
		""" Will generate prices for all cities for all products.

		This method should be used every time there needs to be a rotation in the prices of products, mainly every new
		trade day.

		:return: None, but will update self.prices_in_cities with new prices
		"""
		for city in self.cities_names:
			self.prices_in_cities[city] = ProductsPricesInCity(products_list=self.products_list)
		return None

	def get_prices_in_city_by_city_name(self, city_name: str) -> ProductsPricesInCity:
		""" Will return the prices in a specific city

		:return: ProductsPricesInCity, representing prices in a specific city
		"""
		try:
			prices_in_city: ProductsPricesInCity = self.prices_in_cities[city_name]
			return prices_in_city
		except KeyError:
			raise CustomExceptionCityNameNotFound(f"City {city_name} doesn't exist!")
