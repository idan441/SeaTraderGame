from typing import List
from classes.products import Product, PlayersInventory, PlayerProductInventory
from classes.ship import Ship
from classes.city_prices import ProductsPricesInAllCities, ProductsPricesInCity
from classes.player import Player, PlayersTransaction
from constants import CITIES_LIST, INITIAL_START_CITY, PRODUCTS_LIST, INITIAL_BUDGET, AMOUNT_OF_HOURS_FOR_WORKDAY, \
	TIME_TO_SAIL_BETWEEN_CITIES, TOTAL_TRADE_DAYS_IN_A_GAME


"""
Defines "Game" object representing a whole game of Sea Trader.

Also define "GameResults" object representing the game results
"""


class GameResults:
	""" Represents a result for Sea Trader game """

	def __init__(self,
				 name: str,
				 coins_earned: int,
				 amount_of_trade_days: int):
		"""

		:param name:
		:param coins_earned:
		:param amount_of_trade_days:
		"""
		self.name: str = name
		self.coins_earned: int = coins_earned
		self.amount_of_trade_days: int = amount_of_trade_days


class Game:
	""" Represents a game of Sea Trader, including the player and world status"""

	def __init__(self, player_name: str):
		"""

		:param player_name: Name of the player, will be used solely for output messages
		"""
		# Set constants - imported from constants.py
		self.current_trade_day: int = 1  # First day
		self.hours_left_for_workday: int = AMOUNT_OF_HOURS_FOR_WORKDAY
		self.last_trade_day: int = TOTAL_TRADE_DAYS_IN_A_GAME
		self.time_to_sail_between_cities: int = TIME_TO_SAIL_BETWEEN_CITIES
		self.cities_list: List[str] = CITIES_LIST
		self.products_list: List[Product] = PRODUCTS_LIST

		# Set boolean flags
		self.is_last_trade_day: bool = False  # Will be set to true when player reaches last trade day
		self.is_user_requested_to_finish_game: bool = False  # Set in case player wants to finish game immediately

		# Set objects used to represent the player and game environment
		self.player = Player(name=player_name,
							 initial_budget=INITIAL_BUDGET,
							 initial_location=INITIAL_START_CITY)
		self.player_inventory = PlayersInventory(products_list_in_game=PRODUCTS_LIST)
		self.ship = Ship()
		self.products_prices_in_cities = ProductsPricesInAllCities(cities_names_in_game=self.cities_list,
																   products_in_game=self.products_list)
		self.product_transactions = PlayersTransaction(player=self.player,
													   player_inventory=self.player_inventory,
													   prices_in_city=self.products_prices_in_cities)

	def start_game(self) -> None:
		""" Will start a game and manage it until the end

		:return: None
		"""
		self.start_game_message()

		while self.is_last_trade_day is not True:
			if self.is_user_requested_to_finish_game:
				print("This will be the last trade day as you requested to end game early! ")
				break
			if self.current_trade_day == self.last_trade_day:
				print("This is the last day of trade! Make sure to sell any products left in your ship!")
				self.is_last_trade_day = True

			self.print_current_game_status()
			self.manage_trade_day_menu()
			self.move_to_next_day()

		self.end_game()
		return None

	def manage_trade_day_menu(self):
		""" Allows player to manage options of a trade day.

		:return:
		"""
		print("It's morning of a new trade day. ")
		while True:
			print("Choose an action: "
				  "1) Trade products "
				  "2) Show products price "
				  "3) Show inventory "
				  "4) Show budget "
				  "5) Sail to a new destination "
				  "6) Finish trade day "
				  "7) End game ")
			option_chose: int = int(input())

			if option_chose == 1:
				self.trade_products_menu()
			elif option_chose == 2:
				self.print_products_prices()
			elif option_chose == 3:
				self.print_inventory()
			elif option_chose == 4:
				self.print_current_budget()
			elif option_chose == 5:
				self.sail_to_new_destination_menu()
			elif option_chose == 6:
				break
			elif option_chose == 7:
				self.player_wisheds_to_end_game()
				break
			else:
				print("Wrong option was chosen - try again")

		print("The trade day has finished, you go to sleep.")
		return None

	def sail_to_new_destination_menu(self) -> None:
		""" Manages menu for moving the player between destination - different cities

		:return:
		"""
		print(f"You are currently porting at {self.player.current_location()}")
		print(f"Journey time: {self.time_to_sail_between_cities}")
		print(f"left hours for workday: {self.hours_left_for_workday}")

		if self.hours_left_for_workday < self.time_to_sail_between_cities:
			print(f"It is already too late! You can't sail today! ")
			return None

		while True:
			print(f"Choose a new destination to sail to: ({self.cities_list})")
			new_destination: str = input()
			if new_destination not in self.cities_list:
				print("Wrong destination name! Try again! ")
			elif new_destination == self.player.current_location():
				print("You are already in here!")
				break
			else:
				self.player.set_current_location(new_location=new_destination)
				self.hours_left_for_workday -= self.time_to_sail_between_cities
				print(f"You sailed to {new_destination} the journey took you {self.hours_left_for_workday} hours")
				break

		return None

	def trade_products_menu(self) -> None:
		""" Manages menu for trading (buying/selling) products.

		:return: None
		"""
		print("Choose a product name to trade")
		product_name: str = input()

		product_details: PlayerProductInventory = self.player_inventory.get_product_by_name(product_name=product_name)
		product_price: int = self.products_prices_in_cities. \
			get_prices_in_city_by_city_name(self.player.current_location()) \
			.get_price_for_product(product=product_details.product)

		print(f"You currently have {product_details.amount} of {product_details.product_name}")

		print("Do you want to buy or sell? (Options - buy or sell)")
		action: str = input()

		print(f"Choose amount you want to {action} "
			  f"(Current price at {self.player.current_location()} is {product_price})")
		amount_to_buy_or_sell: int = int(input())

		if action == "buy":
			print(f"Buying {amount_to_buy_or_sell} {product_details.product_name}")
			self.product_transactions.buy_product(product_to_buy=product_details.product,
												  amount_to_buy=amount_to_buy_or_sell)
		elif action == "sell":
			print(f"Selling {amount_to_buy_or_sell} {product_details.product_name}")
			self.product_transactions.sell_product(product_to_sell=product_details.product,
												   amount_to_sell=amount_to_buy_or_sell)
		else:
			print("Wrong option chosen! Try again...")

		print("You just bought/sold!")

		return None

	def print_current_budget(self) -> None:
		""" Prints the current player's budget

		:return: None
		"""
		print(f"You currently have {self.player.get_current_budget()} coins")
		return None

	def print_products_prices(self) -> None:
		""" Prints the products prices in the current city the player is at

		:return:
		"""
		current_city_location: str = self.player.current_location()
		prices_in_city: ProductsPricesInCity = self.products_prices_in_cities. \
			get_prices_in_city_by_city_name(current_city_location)

		print(f"Prices in {current_city_location}:")
		print(f"{prices_in_city.get_prices_of_all_products_as_dict()}")
		return None

	def print_inventory(self) -> None:
		""" Prints the player's inventory

		:return None:
		"""
		products_inventory: List[PlayerProductInventory] = self.player_inventory.get_inventory_content()

		print("Current inventory: ")
		for product in products_inventory:
			print(f"{product.product_name}: {product.amount}")

		return None

	def move_to_next_day(self) -> None:
		""" Moves to next day of trade

		 :return:
		 """
		self.hours_left_for_workday = AMOUNT_OF_HOURS_FOR_WORKDAY
		self.current_trade_day += 1
		self.products_prices_in_cities.generate_prices_for_all_cities()
		return None

	def start_game_message(self):
		""" Prints details for the first time the game starts """
		print(f"Welcome aboard {self.player.name}! You are a captain of a trader ship. "
			  f"You'r task is to make as much profit as you can in the next {self.last_trade_day} days! "
			  f"Good luck! ")
		return None

	def end_game(self) -> GameResults:
		""" Prints a message indicating end of game, including the player's score.

		:return: Game results which can be recorded in the statistics table
		 """
		print(f"Well done captain {self.player.name}! "
			  f"You have earned {self.player.get_current_budget()} coins! ")
		return GameResults(name=self.player.name,
						   coins_earned=self.player.get_current_budget(),
						   amount_of_trade_days=self.current_trade_day)

	def print_current_game_status(self):
		""" Print the current status of the game including the player's details """
		print(f"Trade day is {self.current_trade_day}/{self.last_trade_day}")
		print(f"Current budget is {self.player.get_current_budget()}")
		print(f"Currently you'r ship is anchoring at {self.player.current_location()}")
		print(f"Currently you'r ship health is {self.ship.ship_health}")
		return None

	def player_wisheds_to_end_game(self) -> None:
		""" Will make the game end by setting the current trade day as the last one.
		The method will set flag self.is_user_requested_to_finish_game to True

		:return:
		"""
		self.is_user_requested_to_finish_game = True
		return None
