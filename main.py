from typing import List
from classes.products import Product, PlayersInventory, PlayerProductInventory
from constants import CITIES_LIST, PRODUCTS_LIST, INITIAL_BUDGET, AMOUNT_OF_HOURS_FOR_WORKDAY


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


class Ship:
	""" Represents the player's ship.
	Ship status allows player moving between cities. Ship can break which can prevent the player from sailing between
	cities.
	"""

	def __init__(self):
		"""

		"""
		self.ship_health: int = 100
		self.voyage_time: int = 8  # 4 hours to move between every city


class Player:
	""" Represents the player status. The player is the trader and has a location and budget"""

	def __init__(self, name: str, initial_budget: int, initial_location: str):
		"""

		"""
		self.name: str = name
		self.budget: int = initial_budget
		self._current_location: str = initial_location

	def get_current_budget(self) -> int:
		""" Returns current budget

		:return:
		"""
		return self.budget

	def current_location(self) -> str:
		""" Returns the current location of the player

		:return:
		"""
		return self._current_location

	def set_current_location(self, new_location: str) -> None:
		""" Sets the players location

		:param new_location:
		:return:
		"""
		self._current_location = new_location
		return None

	def add_budget(self, budget_to_add: int) -> None:
		""" Add budget to the player's budget

		:param budget_to_add:
		:return:
		"""
		self.budget += budget_to_add
		return None

	def sub_budget(self, budget_to_remove: int) -> None:
		""" Subtract budget from the player's budget

		:param budget_to_remove:
		:return:
		"""
		self.budget -= budget_to_remove
		return None


class Game:
	""" Represents a game of Sea Trader, including the player and world status"""

	def __init__(self):
		"""

		"""
		self.player = Player(name="example",
							 initial_budget=INITIAL_BUDGET,
							 initial_location="Yafo")
		self.player_inventory = PlayersInventory(products_list_in_game=PRODUCTS_LIST)
		self.ship = Ship()
		self.current_trade_day: int = 0
		self.hours_left_for_workday: int = 16
		self.last_trade_day: int = 21
		self.is_last_trade_day: bool = False

		self.cities_list: List[str] = CITIES_LIST
		self.products_list: List[Product] = PRODUCTS_LIST
		self.start_game_message()

	def start_game(self) -> None:
		""" Will start a game and manage it until the end """
		self.start_game_message()

		while self.is_last_trade_day is not True:
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
			print("Choose an action:"
				  "1 - Trade products"
				  "2 - show inventory"
				  "3 - Finish trade day")
			option_chose: int = int(input())
			if option_chose == 1:
				self.trade_products_menu()
			elif option_chose == 2:
				self.print_inventory()
			elif option_chose == 3:
				break
			else:
				print("Wrong option was chosen - try again")

		print("The trade day has finished, you go to sleep.")
		return None

	def trade_products_menu(self) -> None:
		""" Manages menu for trading (buying/selling) products.

		:return: None
		"""
		print("Choose a product name to trade")
		product_name: str = input()

		product_details: PlayerProductInventory = self.player_inventory.get_product_by_name(product_name=product_name)
		print(f"You currently have {product_details.amount} of {product_details.product_name}")

		print("Do you want to buy or sell? (Options - buy or sell)")
		action: str = input()

		print(f"Choose amount you want to {action}")
		amount_to_buy_or_sell: int = int(input())

		if action == "buy":
			print(f"Buying {amount_to_buy_or_sell} {product_details.product_name}")
			self.player_inventory.add_product_to_inventory(product=product_details.product,
														   amount_to_add=amount_to_buy_or_sell)
		elif action == "sell":
			print(f"Buying {amount_to_buy_or_sell} {product_details.product_name}")
			self.player_inventory.remove_product_from_inventory(product=product_details.product,
																amount_to_remove=amount_to_buy_or_sell)
		else:
			print("Wrong option chosen! Try again...")

		print("You just bought/sold!")

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


def main():
	""" Will ask player for it's details and will start a game of Sea Trader """
	print("Welcome to Sea Trader game")
	print("Sea Trader is a homage to Socher HaYam")
	game = Game()
	game.start_game()


if __name__ == "__main__":
	main()
