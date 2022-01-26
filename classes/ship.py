

"""
Manages player's ship
"""


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
