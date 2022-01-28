import random
from custom_exceptions.ship_custom_exceptions import CustomExceptionWrongVoyageTimeValueForShip


"""
Manages player's ship
"""


class Ship:
	""" Represents the player's ship.
	Ship status allows player moving between cities. Ship can break which can prevent the player from sailing between
	cities.
	"""

	def __init__(self,
				 voyage_time: int,
				 min_fix_cost_in_game: int,
				 max_fix_cost_in_game: int,
				 chance_for_ship_to_break: float,
				 ):
		"""

		:param voyage_time: time in hours to sail between two cities
		:param min_fix_cost_in_game: Minimum price for fixing the ship in case it breaks
		:param max_fix_cost_in_game: Maximum price for fixing the ship in case it breaks
		:param chance_for_ship_to_break: Chance for the ship to break in every voyage, should be between 0 to 1
		"""
		self._is_ship_broken: bool = True
		self._voyage_time: int = voyage_time

		self.fix_cost: int = 0
		self.min_fix_cost_in_game: int = min_fix_cost_in_game
		self.max_fix_cost_in_game: int = max_fix_cost_in_game
		self.chance_for_ship_to_break: float = chance_for_ship_to_break

	def __str__(self) -> str:
		"""

		:return:
		"""
		return f"Ship - is broken: {self._is_ship_broken}, voyage time: {self._voyage_time}, fix cost: {self.fix_cost}"

	@property
	def is_ship_broken(self) -> bool:
		""" Returns the player's ship status

		:return:
		"""
		return self._is_ship_broken

	@property
	def voyage_time(self) -> int:
		""" Returns the voyage time of the ship between two cities in game

		:return:
		"""
		return self._voyage_time

	def do_random_event_damage_ship(self) -> None:
		""" Will do a random event which can break the ship. If ship breaks then the player can't keep sailing between
		ports until he fixes it. Also in case damage occurs will set a price for fixing the damage.

		:return: Boolean - true in case ship breaks, else false
		"""
		random_break_int: float = random.randint(0, 100) / 100
		if random_break_int < self.chance_for_ship_to_break:
			# In case random number is smaller than break chance - break ship
			self._is_ship_broken = False
			self.fix_cost = random.randint(self.min_fix_cost_in_game, self.max_fix_cost_in_game)

		return None

	def fix_ship(self) -> None:
		""" Will fix the ship.
		Should be triggered by the Game class and after removing the fix cost from the player

		:return: None
		"""
		self._is_ship_broken = True
		self.fix_cost = 0
		return None

	def upgrade_ship_voyage_time(self, new_voyage_time: int) -> None:
		""" Should upgrade the ship, allowing it to have faster voyage time between different cities.

		:param new_voyage_time: New voyage time - should be smaller than current one
		:return: None, in case new voyage time is bigger/equals to existing voyage time - an exception will raise
		"""
		if new_voyage_time < self._voyage_time:
			self._voyage_time = new_voyage_time
		else:
			raise CustomExceptionWrongVoyageTimeValueForShip(f"Wrong voyage time given ({new_voyage_time}) - should be"
															 f"smaller than current voyage time ({self._voyage_time})")
		return None
