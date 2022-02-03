

"""
Contains GameResults object which represents a single result of the game
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
