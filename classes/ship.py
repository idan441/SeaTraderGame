import logging
import random
from custom_exceptions.ship_custom_exceptions import CustomExceptionWrongVoyageTimeValueForShip

logger = logging.getLogger(__name__)

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
				 ship_upgrade_time_by_hours: int,
				 ):
		"""

		:param voyage_time: time in hours to sail between two cities
		:param min_fix_cost_in_game: Minimum price for fixing the ship in case it breaks
		:param max_fix_cost_in_game: Maximum price for fixing the ship in case it breaks
		:param chance_for_ship_to_break: Chance for the ship to break in every voyage, should be between 0 to 1
		:param ship_upgrade_time_by_hours: The amount of time to be reduced from the ship voyage time per upgrade
		"""
		self._is_ship_broken: bool = False
		self._voyage_time: int = voyage_time

		self.fix_cost: int = 0
		self.min_fix_cost_in_game: int = min_fix_cost_in_game
		self.max_fix_cost_in_game: int = max_fix_cost_in_game
		self.chance_for_ship_to_break: float = chance_for_ship_to_break
		self.ship_upgrade_time_by_hours: int = ship_upgrade_time_by_hours

		logger.info(f"Initiated player ship with following details - "
					f"fix cost: {self.fix_cost} "
					f"min_fix_cost_in_game: {self.min_fix_cost_in_game} "
					f"max_fix_cost_in_game: {self.max_fix_cost_in_game} "
					f"chance_for_ship_to_break: {self.chance_for_ship_to_break} "
					f"voyage time: {self._voyage_time} "
					f"ship upgrade time by hours: {self.ship_upgrade_time_by_hours}")

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

	def do_random_event_damage_ship(self) -> bool:
		""" Will do a random event which can break the ship. If ship breaks then the player can't keep sailing between
		ports until he fixes it. Also in case damage occurs will set a price for fixing the damage.

		:return: Boolean - true in case ship breaks, else false
		"""
		random_break_int: float = random.randint(0, 100) / 100
		if random_break_int < self.chance_for_ship_to_break:
			# In case random number is smaller than break chance - break ship
			self._is_ship_broken = True
			self.fix_cost = random.randint(self.min_fix_cost_in_game, self.max_fix_cost_in_game)
			logger.info(f"Ship broke - cost fix: {self.fix_cost} , chance to break: {self.chance_for_ship_to_break}")
			return True
		return False

	def fix_ship(self) -> None:
		""" Will fix the ship.
		Should be triggered by the Game class and after removing the fix cost from the player

		:return: None
		"""
		self._is_ship_broken = False
		self.fix_cost = 0
		logger.debug("Ship fixed by player!")
		return None

	def upgrade_ship_voyage_time(self) -> None:
		""" Should upgrade the ship, allowing it to have faster voyage time between different cities.

		Ship upgrade will reduce it's voyage time by a constants time amount defined at self.ship_upgrade_time_by_hours

		Voyage time must always be 1 hour or longer! 0 or negative voyage times are not allowed!

		:return: None, but will raise an exception in case ship can't be further upgraded
		"""
		if self.is_ship_upgradeable():
			new_voyage_time: int = self._voyage_time - self.ship_upgrade_time_by_hours
			self._voyage_time = new_voyage_time
		else:
			error_message: str = "Failed upgrading the ship! Ship can not be upgrade anymore!" \
								 f"Current voyage time: {self._voyage_time}"
			logger.error(error_message)
			raise CustomExceptionWrongVoyageTimeValueForShip(error_message)
		return None

	def is_ship_upgradeable(self) -> bool:
		""" Check if the ship voyage time can be further upgraded. Ship voyage time must always be at least one hour!
		( As zero time will give player unlimited travels per day and it doesn't make sense! Negative time will
		elongate the game which doesn't make sense )

		:return: Boolean - true if the ship can be further upgraded
		"""
		new_voyage_time: int = self._voyage_time - self.ship_upgrade_time_by_hours
		if new_voyage_time >= 1:
			return True
		return False
