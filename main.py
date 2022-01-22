from typing import List
from constants import CITIES_LIST, INITIAL_BUDGET, AMOUNT_OF_HOURS_FOR_WORKDAY


class Game:
	""" Represents a game of Sea Trader, including the player and world status"""

	def __init__(self):
		"""

		"""
		self.player = Player(name="example",
							 initial_budget=INITIAL_BUDGET,
							 initial_location="Yafo")
		self.ship = Ship()
		self.current_trade_day: int = 0
		self.hours_left_for_workday: int = 16
		self.last_trade_day: int = 21
		self.is_last_trade_day: bool = False

		self.cities_list: List[str] = CITIES_LIST
		self.start_game()

	def move_to_next_day(self):
		""" Moves to next day of trade """
		self.hours_left_for_workday = AMOUNT_OF_HOURS_FOR_WORKDAY
		self.current_trade_day += 1

		if self.current_trade_day == self.is_last_trade_day:
			print("This is the last day of trade! Make sure to sell any products left in your ship!")
			self.is_last_trade_day = True

	def start_game(self):
		""" Prints details for the first time the game starts """
		print(f"Welcome aboard {self.player.name}! You are a captain of a trader ship. "
			  f"You'r task is to make as much profit as you can in the next {self.last_trade_day} days! "
			  f"Good luck! ")

	def end_game(self):
		pass

	def print_current_game_status(self):
		""" Print the current status of the game including the player's details """
		print(f"Trade day is {self.current_trade_day}/{self.last_trade_day}")
		print(f"Current budget is {self.player.get_current_budget()}")
		print(f"Currently you'r ship is anchoring at {self.player.current_location()}")


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


def main():
	""" Will ask player for it's details and will start a game of Sea Trader """
	print("Welcome to Sea Trader game")
	print("Sea Trader is a homage to Socher HaYam")
	game = Game()
	game.print_current_game_status()
	game.move_to_next_day()
	game.print_current_game_status()


if __name__ == "__main__":
	main()
