import logging
from classes.city_prices import ProductsPricesInAllCities, ProductsPricesInCity
from classes.products import PlayerProductInventory, PlayersInventory
from custom_exceptions.product_custom_exceptions import CustomExceptionPlayerHasNotEnoughBudget, \
	CustomExceptionsTransactionFailNotEnoughItemAmount


logger = logging.getLogger(__name__)


"""
Manages player object + related functionalities
"""


class Player:
	""" Represents the player status. The player is the trader and has a location and budget"""

	def __init__(self, name: str, initial_budget: int, initial_location: str):
		"""

		"""
		self.name: str = name
		self._budget: int = initial_budget
		self._current_location: str = initial_location

		logger.info(f"Initiated player for the game with following details - "
					f"name: {self.name} , budget: {self._budget} , current_location: {self._current_location}")

	@property
	def location(self) -> str:
		""" Returns the current location of the player

		:return:
		"""
		return self._current_location

	@location.setter
	def location(self, new_location: str):
		""" Sets the players location

		:param new_location:
		:return:
		"""
		self._current_location = new_location

	@property
	def budget(self) -> int:
		""" Returns player's current budget

		:return:
		"""
		return self._budget

	def add_budget(self, budget_to_add: int) -> None:
		""" Add budget to the player's budget

		:param budget_to_add:
		:return:
		"""
		logger.debug(f"Will change player budget - current budget {self._budget} , should add {budget_to_add}")
		self._budget += budget_to_add
		logger.debug(f"Changed player budget is {self._budget}")
		return None

	def sub_budget(self, budget_to_remove: int) -> None:
		""" Subtract budget from the player's budget

		:param budget_to_remove:
		:return:
		"""
		logger.debug(f"Changed player budget - current budget {self._budget} , should remove {budget_to_remove}")
		if self._budget < budget_to_remove:
			raise CustomExceptionPlayerHasNotEnoughBudget("Player has not enough budget! "
														  f"Current budget: {self._budget} , "
														  f"amount to remove: {budget_to_remove}")
		self._budget -= budget_to_remove
		logger.debug(f"Changed player budget - new budget {self._budget}")
		return None


class PlayersTransaction:
	""" Used to make transactions with player's budget as well as his inventory.
	Should be used to sell/buy products and changing the player's budget accordingly."""
	def __init__(self,
				 player: Player,
				 player_inventory: PlayersInventory,
				 prices_in_city: ProductsPricesInAllCities):
		"""

		:param player: A Player object representing the player in the game. The PLayer object represents the player's
					   current budget
		:param player_inventory: An object representing the player's inventory in the game.
		:param prices_in_city: An object representing the prices for the different products in the different cities
		"""
		self.player: Player = player
		self.player_inventory: PlayersInventory = player_inventory
		self.prices_in_city: ProductsPricesInAllCities = prices_in_city

	def check_player_has_enough_budget(self, needed_amount_of_cash: int) -> bool:
		""" Check if a number, representing a buy transaction, is bigger than the player's budget.

		:param needed_amount_of_cash:
		:return: Boolean - true if player has enough cash to do a buy transaction
		"""
		if needed_amount_of_cash <= self.player.budget:
			return True
		return False

	def remove_money_from_player(self, amount_to_remove: int) -> None:
		""" Will remove money from the player's budget.
		This will be used to cover extra costs for player not related to products trading - like fixing the ship.

		:param amount_to_remove:
		:return: None, but will raise an exception in case player has not enough budget
		"""
		self.player.sub_budget(amount_to_remove)
		return None

	def buy_product(self, product_to_buy: PlayerProductInventory, amount_to_buy: int) -> None:
		""" Will do a buy transaction for a player.

		:param product_to_buy:
		:param amount_to_buy:
		:return: True on success, in case the player has not enough budget - will return false.
		"""
		prices_in_city: ProductsPricesInCity = \
			self.prices_in_city.get_prices_in_city_by_city_name(city_name=self.player.location)

		product_price: int = prices_in_city.get_price_for_product(product=product_to_buy)
		cost: int = amount_to_buy * product_price
		if self.check_player_has_enough_budget(cost):
			self.player_inventory.add_product_to_inventory(product=product_to_buy,
														   amount_to_add=amount_to_buy)
			self.player.sub_budget(budget_to_remove=cost)
			return None
		else:
			raise CustomExceptionPlayerHasNotEnoughBudget(f"Player has not enough of budget to buy {amount_to_buy} X "
														  f"{product_to_buy.name} - in a cost of {cost}")

	def sell_product(self, product_to_sell: PlayerProductInventory, amount_to_sell: int) -> None:
		""" Will do a sell transaction for a player.

		:param product_to_sell:
		:param amount_to_sell:
		:return: None on success of transaction, in case the player has not enough of the product to sell - will raise
		         an exception
		"""
		prices_in_city: ProductsPricesInCity = \
			self.prices_in_city.get_prices_in_city_by_city_name(city_name=self.player.location)

		product_price: int = prices_in_city.get_price_for_product(product=product_to_sell)
		profit: int = amount_to_sell * product_price
		if self.player_inventory.check_if_amount_of_item_exists_in_inventory(product=product_to_sell,
																			 amount=amount_to_sell):
			self.player_inventory.remove_product_from_inventory(product=product_to_sell,
														   		amount_to_remove=amount_to_sell)
			self.player.add_budget(budget_to_add=profit)
			return None
		else:
			raise CustomExceptionsTransactionFailNotEnoughItemAmount(f"Can't do a sell transaction for {amount_to_sell}"
																	 f" X {product_to_sell.name} "
																	 f"- because the player has not enough of it. ")
