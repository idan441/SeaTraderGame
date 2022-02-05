from typing import Dict, Union
from datetime import datetime

"""
Contains GameResult object which represents a single result of the game
"""


class GameResult:
	""" Represents a result for Sea Trader game """

	def __init__(self,
				 name: str,
				 coins_earned: int,
				 amount_of_trade_days: int,
				 game_datetime: datetime = datetime.now()):
		"""

		:param name: player's name
		:param coins_earned: coins earned at end of game. (Profit)
		:param amount_of_trade_days: Number of trade days in game
		:param game_datetime: datetime when the game finished, else will take current datetime as default value
		"""
		self.name: str = name
		self.coins_earned: int = coins_earned
		self.amount_of_trade_days: int = amount_of_trade_days
		self.game_datetime: datetime = game_datetime

	def __str__(self) -> str:
		""" Prints a formatted string with the game score

		:return: str
		"""
		return f"Game score: player {self.name} has scored {self.coins_earned} in {self.amount_of_trade_days} days. " \
			   f"( Game time is {str(self.game_datetime).split('.')[0]} )"

	def get_game_result_as_dict(self) -> Dict[str, Union[str, int, datetime]]:
		""" Will return a dictionary with the game result
		Used by HighScoresMenu to print the game high-scores

		:return: Dict
		"""
		game_result: Dict[str, Union[str, int, datetime]] = {
			"Name": self.name,
			"Coins earned": self.coins_earned,
			"Amount of trade days": self.amount_of_trade_days,
			"Game date": self.game_datetime
		}
		return game_result
