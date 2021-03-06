from typing import List, Dict, Union
import logging
from tabulate import tabulate
from classes.products import Product, PlayersInventory, PlayerProductInventory
from classes.ship import Ship
from classes.city_prices import ProductsPricesInAllCities, ProductsPricesInCity
from classes.player import Player, PlayersTransaction
from highscores.game_result import GameResult
from constants import CITIES_LIST, INITIAL_START_CITY, PRODUCTS_LIST, INITIAL_BUDGET, AMOUNT_OF_HOURS_FOR_WORKDAY, \
	TOTAL_TRADE_DAYS_IN_A_GAME, SHIP_TIME_TO_SAIL_BETWEEN_CITIES, SHIP_MINIMUM_FIX_COST_IN_GAME, \
	SHIP_MAXIMUM_FIX_COST_IN_GAME, CHANCE_FOR_SHIP_TO_BREAK, SHIP_UPGRADE_TIME_HOURS_REDUCTION, SHIP_UPGRADE_PRICE, \
	SHIP_UPGRADE_TIME_AT_SHIPYARD
from input_handling.user_input import UserInput
from custom_exceptions.product_custom_exceptions import CustomExceptionPlayerHasNotEnoughBudget, \
	CustomExceptionsTransactionFailNotEnoughItemAmount

"""
Defines "Game" object representing a whole game of Sea Trader.
"""

logger = logging.getLogger(__name__)


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
		self.cities_list: List[str] = CITIES_LIST
		self.products_list: List[Product] = PRODUCTS_LIST

		# Set boolean flags
		self.is_last_trade_day: bool = False  # Will be set to true when player reaches last trade day
		self.is_user_requested_to_finish_game: bool = False  # Set in case player wants to finish game immediately

		# Set objects used to represent the player and game environment
		self.player = Player(
			name=player_name,
			initial_budget=INITIAL_BUDGET,
			initial_location=INITIAL_START_CITY)
		self.player_inventory = PlayersInventory(
			products_list_in_game=PRODUCTS_LIST)
		self.ship = Ship(
			voyage_time=SHIP_TIME_TO_SAIL_BETWEEN_CITIES,
			min_fix_cost_in_game=SHIP_MINIMUM_FIX_COST_IN_GAME,
			max_fix_cost_in_game=SHIP_MAXIMUM_FIX_COST_IN_GAME,
			chance_for_ship_to_break=CHANCE_FOR_SHIP_TO_BREAK,
			ship_upgrade_time_by_hours=SHIP_UPGRADE_TIME_HOURS_REDUCTION,
			ship_upgrade_work_time_by_hours=SHIP_UPGRADE_TIME_AT_SHIPYARD)

		self.products_prices_in_cities = ProductsPricesInAllCities(
			cities_names_in_game=self.cities_list,
			products_in_game=self.products_list)
		self.product_transactions = PlayersTransaction(
			player=self.player,
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

			self.manage_trade_day_menu()
			self.move_to_next_day()

		self.end_game()
		return None

	def manage_trade_day_menu(self) -> None:
		""" Allows player to manage options of a trade day.

		:return: None
		"""
		print("It's morning of a new trade day. ")
		self.print_current_game_status()

		while True:
			option_chose: int = UserInput.get_user_number_input_for_menu(
				prompt_message="Choose an option from these: ",
				options_dict={
					1: "Trade products",
					2: "Show products price and current inventory",
					3: "Show budget",
					4: "Sail to a new destination",
					5: "Game status (location, work days left, trade day number, budget)",
					6: "Ship status (fix / upgrade ship)",
					7: "Finish trade day",
					8: "End game",
				}
			)

			if option_chose == 1:
				self.trade_products_menu()
			elif option_chose == 2:
				self.print_products_prices_and_player_inventory()
			elif option_chose == 3:
				self.print_current_budget()
			elif option_chose == 4:
				self.sail_to_new_destination_menu()
			elif option_chose == 5:
				self.print_current_game_status()
			elif option_chose == 6:
				self.ship_management_menu()
			elif option_chose == 7:
				break
			elif option_chose == 8:
				self.player_wishes_to_end_game()
				break

		print("The trade day has finished, you go to sleep.")
		return None

	def sail_to_new_destination_menu(self) -> None:
		""" Manages menu for moving the player between destination - different cities

		:return: None
		"""
		self.print_player_location_and_time_details()

		if self.hours_left_for_workday < self.ship.voyage_time:
			print(f"It is already too late! You can't sail today! ")
			return None
		elif self.ship.is_ship_broken:
			print("Your ship is broken - you can't sail until it will be fixed!")
			return None

		while True:
			STAY_HERE_OPTION: List[str] = ["Stay here"]
			new_destination: str = UserInput.get_user_string_input(
				prompt_message=f"Choose a new destination to sail to:",
				options_list=self.cities_list + STAY_HERE_OPTION,
				is_case_sensitive=False,
			)

			# Check the player is eligible for the voyage
			if new_destination in STAY_HERE_OPTION:
				print(f"You choose to stay at {self.player.location}")
				break
			if new_destination not in self.cities_list:
				print("Wrong destination name! Try again! ")
			elif new_destination == self.player.location:
				print("You are already in here!")
				break
			elif self.ship.is_ship_broken:
				print("Your ship is broken - you can't sail with it until it will be fixed!")
				break
			# In case player is eligible for the voyage
			else:
				if self.ship.do_random_event_damage_ship():
					print("Your ship got broken while doing the journey! "
						  "You need to fix it in order to be able to set sail again!")

				self.player.location = new_destination
				self.hours_left_for_workday -= self.ship.voyage_time
				print(f"You sailed to {new_destination} the journey took you {self.ship.voyage_time} hours")

				break

		return None

	def ship_management_menu(self) -> None:
		""" Manages menu for player's ship details - status, fix and improve options.

		:return: None
		"""
		print("Ship management menu")
		print("Welcome to the shipyard, how can we help you?")
		while True:
			option_chose: int = UserInput.get_user_number_input_for_menu(
				prompt_message="Choose an option from these: ",
				options_dict={
					1: "Ship status",
					2: "Fix ship",
					3: "Upgrade ship",
					4: "Back to former menu",
				}
			)

			if option_chose == 1:
				self.print_ship_status()
			elif option_chose == 2:
				self.fix_ship_menu()
			elif option_chose == 3:
				self.upgrade_ship_menu()
			elif option_chose == 4:
				break
		return None

	def trade_products_menu(self) -> None:
		""" Manages menu for trading (buying/selling) products.

		:return: None
		"""
		while True:
			option_chose: int = UserInput.get_user_number_input_for_menu(
				prompt_message="Choose an option from these: ",
				options_dict={
					1: "Buy products",
					2: "Sell products",
					3: "Show player's inventory and current product prices",
					4: "Show current budget",
					5: "Back to former menu",
				}
			)

			if option_chose == 1:
				self.buy_sell_product_menu(action="buy")
			elif option_chose == 2:
				self.buy_sell_product_menu(action="sell")
			elif option_chose == 3:
				self.print_products_prices_and_player_inventory()
			elif option_chose == 4:
				self.print_current_budget()
			elif option_chose == 5:
				break

		return None

	def buy_sell_product_menu(self, action: str = Union["buy", "sell"]) -> None:
		""" Menu for buying or selling a single product from the player's inventory

		:param action: Action to do - "buy" or "sell"
		:return: None
		"""
		player_location: str = self.player.location

		product_name: str = UserInput.get_user_string_input(
			prompt_message=f"Choose a product name to {action}",
			options_list=[product.name for product in self.products_list],
			is_case_sensitive=False
		)

		product_details: PlayerProductInventory = self.player_inventory.get_product_by_name(product_name=product_name)

		product_price_at_city: int = self.products_prices_in_cities. \
			get_prices_in_city_by_city_name(player_location) \
			.get_price_for_product(product=product_details.product)

		print(f"You currently have {product_details.amount} of {product_details.product_name}")

		amount_to_buy_or_sell: int = UserInput.get_user_numeric_input(
			prompt_message=f"Choose amount you want to {action} "
						   f"(Current {product_details.product_name} price at {player_location} "
						   f"is {product_price_at_city})",
			min_value=0
		)
		transaction_cost: int = amount_to_buy_or_sell * product_price_at_city

		logger.info(f"User requested to {action}: item {product_details.product_name} , "
					f"amount {amount_to_buy_or_sell}, price {product_price_at_city}")

		if action == "buy":
			is_to_buy: bool = UserInput.get_user_yes_no_input(
				prompt_message=f"Buy {amount_to_buy_or_sell} X {product_details.product_name}? ("
							   f"Total price {product_price_at_city * amount_to_buy_or_sell} , "
							   f"will leave you with {self.player.budget - (transaction_cost)})"
			)
			if is_to_buy:
				try:
					self.product_transactions.buy_product(product_to_buy=product_details.product,
														  amount_to_buy=amount_to_buy_or_sell)
					print(f"You just bought {amount_to_buy_or_sell} X {product_details.product_name}!")
				except CustomExceptionPlayerHasNotEnoughBudget:
					print(f"You don't have enough of budget to buy that much {product_details.product_name}")

		elif action == "sell":
			is_to_sell: bool = UserInput.get_user_yes_no_input(
				prompt_message=f"Sell {amount_to_buy_or_sell} X {product_details.product_name}? ("
							   f"You now have {product_details.amount} {product_details.product_name} and will stay "
							   f"with {product_details.amount - amount_to_buy_or_sell} X {product_details.product_name}. "
							   f"You will gavin total of {transaction_cost} coins profit ) "
			)
			if is_to_sell:
				try:
					self.product_transactions.sell_product(product_to_sell=product_details.product,
														   amount_to_sell=amount_to_buy_or_sell)
					print(f"You just sold {amount_to_buy_or_sell} X {product_details.product_name}!")
				except CustomExceptionsTransactionFailNotEnoughItemAmount:
					print(f"You don't have enough {product_details.product_name} to sell! "
						  f"( You have {product_details.amount} {product_details.product_name} )")

		return None

	def upgrade_ship_menu(self) -> None:
		""" Will allow to upgrade the ship voyage time to be faster

		As much as the ship is faster then its travelling time will be faster. This will allow player to sail between
		more destinations in a single trade day.

		Upgrading the ship requires work-hours (i.e. time when player can't trade or sail) and costs budget. The values
		for these parameters are defined at constants.py file

		:return: None
		"""
		print(f"You current speed velocity is {self.ship.voyage_time} hours.")

		if not self.ship.is_ship_upgradeable():
			print("Ship reached best voyage time available! Can't upgrade the ship anymore! ")
			return None

		ship_upgrade_price: int = SHIP_UPGRADE_PRICE
		print(f"You can reduce it by {self.ship.ship_upgrade_time_by_hours} hour "
			  f"for a payment of {ship_upgrade_price} coins. "
			  f"The time taken for upgrading the ship is {self.ship.ship_upgrade_work_time_by_hours} hours. ")

		is_to_upgrade_ship: bool = UserInput.get_user_yes_no_input(
			prompt_message=f"Do you want to upgrade the ship for {ship_upgrade_price} coins?"
		)

		if self.hours_left_for_workday < self.ship.ship_upgrade_work_time_by_hours:
			print(f"It is already too late - not enough work hours to upgrade the ship today! Try tomorrow... ")
			return None

		if is_to_upgrade_ship:
			try:
				self.product_transactions.remove_money_from_player(amount_to_remove=ship_upgrade_price)
				self.hours_left_for_workday -= self.ship.ship_upgrade_work_time_by_hours
				self.ship.upgrade_ship_voyage_time()
				print(f"Your ship is now upgraded! You can now sail between cities in {self.ship.voyage_time} hours!")
			except CustomExceptionPlayerHasNotEnoughBudget:
				print("You don't have enough of money to pay for upgrading your ship!")

		return None

	def fix_ship_menu(self) -> None:
		""" Print a menu to manage fix of broken ship

		:return: None
		"""
		if not self.ship.is_ship_broken:
			print("Your ship is healthy, no need to fix it.")
			return None

		print(f"The cost to fix the ship is {self.ship.fix_cost}")

		is_to_fix: bool = UserInput.get_user_yes_no_input(
			prompt_message=f"Do you want to fix the ship for {self.ship.fix_cost} coins?"
		)
		if is_to_fix:
			try:
				self.product_transactions.remove_money_from_player(amount_to_remove=self.ship.fix_cost)
				self.ship.fix_ship()
				print("Your ship is fixed! You can sail again between cities.")
			except CustomExceptionPlayerHasNotEnoughBudget:
				print("You don't have enough of money to pay the cost of fixing ship!")

		return None

	def print_ship_status(self) -> None:
		""" Prints ship status

		:return: None
		"""
		print(f"Your ship is currently at {self.player.location}")
		print(f"Time to sail between two cities is: {self.ship.voyage_time}")
		if self.ship.is_ship_broken:
			print(f"Your ship is broken! You need to fix it in order to be able to sail.")
			print(f"The cost to fix the ship is {self.ship.fix_cost}")
		else:
			print("Your ship is healthy! You can sail to any city you want")

		return None

	def print_player_location_and_time_details(self) -> None:
		""" Prints the location details - current location of player, time at day, hours left for the day

		:return None
		"""
		print(f"You are currently porting at {self.player.location}")
		print(f"Journey time: {self.ship.voyage_time}")
		print(f"left hours for workday: {self.hours_left_for_workday}")
		return None

	def print_current_budget(self) -> None:
		""" Prints the current player's budget

		:return: None
		"""
		print(f"You currently have {self.player.budget} coins")
		return None

	def print_products_prices_and_player_inventory(self) -> None:
		""" Prints the products prices in the current city the player is at, including their possible price range in
		game and the amount the player hold of them.

		:return: None
		"""
		current_city_location: str = self.player.location
		prices_in_city: ProductsPricesInCity = self.products_prices_in_cities. \
			get_prices_in_city_by_city_name(current_city_location)
		products_prices_in_city: Dict[str, int] = prices_in_city.get_prices_of_all_products_as_dict()

		# Order the products and get their amount in player inventory - and print it
		products_list_to_print: List[Dict[str, Union[str, int]]] = []
		for product, price in products_prices_in_city.items():
			product_inventory: PlayerProductInventory = self.player_inventory.get_product_by_name(product_name=product)
			product_price_details: Product = product_inventory.product
			products_list_to_print.append(
				{
					"Product": product,
					"Current price": price,
					"Your inventory": product_inventory.amount,
					"Total worth": price * product_inventory.amount,
					"Product price range": f"{product_price_details.min_price}-{product_price_details.max_price}",
				}
			)

		print(f"Prices in {current_city_location}:")
		print(tabulate(tabular_data=products_list_to_print, headers="keys"))
		return None

	def move_to_next_day(self) -> None:
		""" Moves to next day of trade

		 :return: None
		 """
		self.hours_left_for_workday = AMOUNT_OF_HOURS_FOR_WORKDAY
		self.current_trade_day += 1
		self.products_prices_in_cities.generate_prices_for_all_cities()
		return None

	def start_game_message(self) -> None:
		""" Prints details for the first time the game starts

		:return: None
		"""
		print(f"Welcome aboard {self.player.name}! You are a captain of a trader ship. "
			  f"Your task is to make as much profit as you can in the next {self.last_trade_day} trading days!\n"
			  f"Good luck!\n")
		return None

	def end_game(self) -> None:
		""" Prints a message indicating end of game, including the player's score.

		:return: None
		 """
		print(f"Well done captain {self.player.name}! "
			  f"You have earned {self.player.budget} coins! ")
		return None

	def print_current_game_status(self) -> None:
		""" Print the current status of the game including: trade day, player's budget, player's location, work hours
		left for the day and the ship status if it is broken.

		:return: None
		"""
		print(f"Currently your ship is anchoring at {self.player.location}. \n"
			  f"Trade day is {self.current_trade_day}/{self.last_trade_day} "
			  f"and there are {self.hours_left_for_workday} work hours left. \n"
			  f"Current budget is {self.player.budget} coins. ")
		if self.ship.is_ship_broken:
			print(f"Your ship is broken! You need to fix it in order to be able to sail.")
		return None

	def player_wishes_to_end_game(self) -> None:
		""" Will make the game end by setting the current trade day as the last one.
		The method will set flag self.is_user_requested_to_finish_game to True

		:return: None
		"""
		is_to_end_game: bool = UserInput.get_user_yes_no_input(
			prompt_message="Are you sure you want to finish the game now? ( This will get you to the latest trade day )"
		)
		if is_to_end_game:
			self.is_user_requested_to_finish_game = True
		return None

	@property
	def game_results(self) -> GameResult:
		""" Returns the game results which can be recorded in the statistics table

		:return: GameResult object
		"""
		return GameResult(name=self.player.name,
						  coins_earned=self.player.budget,
						  amount_of_trade_days=self.current_trade_day)
