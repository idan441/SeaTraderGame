from typing import List, Dict, Union
import json
from datetime import datetime
from pathlib import Path
from highscores.game_result import GameResult
from constants import GAME_HIGH_SCORES_FILE_PATH

"""
Contains functionality for managing the high scores table
"""


class HighScoresFileFieldsNames:
	""" Fields names used by the JSON file holding the game high scores
	Class is used solely by ManageHighScoresFile object defined below """
	NAME: str = "name"
	COINS_EARNED: str = "coins_earned"
	AMOUNT_OF_TRADE_DAYS: str = "amount_of_trade_days"
	GAME_DATETIME: str = "game_datetime"


class ManageHighScoresFile:
	def __init__(self):
		""" Game high scores will be stored in a file on the OS volume. The file will contains a JSON string containing
		the game results. This class will allow to read and write the file, and to transfer the JSON string to a list
		of GameResult objects which represent the player's games scores.

		File should look like this - List[Dict[str, str]
		[
		{"name": "player_name",
		 "coins_earned": 200,
		 "amount_of_trade_days": 10,
		 "game_datetime": <datetime>}
		 ...
		]

		"""
		self.high_scores_file_path: str = GAME_HIGH_SCORES_FILE_PATH
		self.high_scores_file: Path = Path(self.high_scores_file_path)

	def is_high_scores_file_exist(self) -> bool:
		""" Checks if the high scores file exists

		:return: Boolean - true if file exists
		"""
		if self.high_scores_file.is_file():
			return True
		return False

	def read_high_scores_data_from_file(self) -> List[Dict[str, Union[str, int, datetime]]]:
		""" Will return the high scores file content - as a string.

		File will still need to be formatted from JSON to a list of GameResult objects

		:return: str
		"""
		game_high_scores_as_json = ""
		try:
			file_content: str = self.high_scores_file.read_text()
			game_high_scores_as_json = json.loads(file_content)
		except FileNotFoundError:
			print(f"Couldn't find a game high-scores file at {self.high_scores_file_path} - "
				  f"will not return high-scores details")
		return game_high_scores_as_json

	def get_high_scores_from_file(self) -> List[GameResult]:
		""" Will return games high-scores data, based on the data file storing them

		:return: A list of game results, to be used by HighScores object
		"""
		game_high_scores_as_json = self.read_high_scores_data_from_file()
		games_results: List[GameResult] = []

		try:
			for game_result_details_in_json in game_high_scores_as_json:
				name: str = game_result_details_in_json[HighScoresFileFieldsNames.NAME]
				coins_earned: int = game_result_details_in_json[HighScoresFileFieldsNames.COINS_EARNED]
				amount_of_trade_days: int = game_result_details_in_json[HighScoresFileFieldsNames.AMOUNT_OF_TRADE_DAYS]
				game_datetime: datetime = game_result_details_in_json[HighScoresFileFieldsNames.GAME_DATETIME]

				games_results.append(
					GameResult(name=name,
							   coins_earned=coins_earned,
							   amount_of_trade_days=amount_of_trade_days,
							   game_datetime=game_datetime)
				)
		except Exception as e:
			print(f"no results in file or bad format! {e}")

		return games_results

	def update_high_scores_file(self, game_results_list: List[GameResult]) -> None:
		""" Will update the high scores file with the current game high scores.

		High scores file will include a JSON string with all results with this structure:

		:return: None
		"""
		game_results_dict_formatted: List[Dict[str, any]] = self.format_game_results_to_json_string(
			game_results_list=game_results_list
		)
		game_results_as_text_string: str = json.dumps(
			game_results_dict_formatted,
			indent=4,
			sort_keys=True,
			default=str
		)
		with self.high_scores_file.open("w", encoding="utf-8") as file:
			file.write(game_results_as_text_string)
		return None

	@staticmethod
	def format_game_results_to_json_string(game_results_list: List[GameResult]) -> List[Dict[str, any]]:
		""" This will take the game results and will format them to a JSON string which can be saved in the games
		high scores file.

		This method is used by method self.update_high_scores_file()

		:return: List[Dict[str, any]] - based on the games high-score - which be saved on machine for future games
		"""
		game_results_dict_formatted: List[Dict[str, any]] = []
		for game_result in game_results_list:
			game_results_dict_formatted.append(
				{
					HighScoresFileFieldsNames.NAME: game_result.name,
					HighScoresFileFieldsNames.COINS_EARNED: game_result.coins_earned,
					HighScoresFileFieldsNames.AMOUNT_OF_TRADE_DAYS: game_result.amount_of_trade_days,
					HighScoresFileFieldsNames.GAME_DATETIME: game_result.game_datetime
				}
			)

		return game_results_dict_formatted


class HighScores:
	""" Will manage the game's high score table """

	def __init__(self):
		"""

		"""
		self._game_results: List[GameResult] = []
		self.manage_high_scores_file_helper = ManageHighScoresFile()
		self.get_game_results_from_file()

	@property
	def game_results(self) -> List[GameResult]:
		""" Returns a list with games high-scores

		:return: List[GameResult]
		"""
		return self._game_results

	def get_game_results_ordered_by_score(self) -> List[GameResult]:
		""" Will return game results ordered by cash profit at end of game in ascending order

		:return: A list of all game results ordered by cash profit
		"""
		game_results_ordered_by_coins_earned: List[GameResult] = sorted(
			self._game_results,
			key=lambda game_result: game_result.coins_earned,
			reverse=True
		)
		return game_results_ordered_by_coins_earned

	def get_game_results_ordered_by_date(self) -> List[GameResult]:
		""" Will return game results ordered by date games played in ascending order

		:return: A list of all game results ordered by game dates
		"""
		game_results_ordered_by_date: List[GameResult] = sorted(
			self._game_results,
			key=lambda game_result: game_result.game_datetime,
			reverse=True
		)
		return game_results_ordered_by_date

	def add_new_game_result(self, game_result: GameResult) -> None:
		""" Will add a game result to the high-scores. Als will update the high scores file so the result will be shown
		in future when the game is running.

		:return: None
		"""
		self._game_results.append(game_result)
		self.update_game_results_file()
		return None

	def update_game_results_file(self) -> None:
		""" Updates the game results in a physical file on the machine so it will be kept for future games.

		:return: None
		"""
		self.manage_high_scores_file_helper.update_high_scores_file(game_results_list=self._game_results)
		return None

	def get_game_results_from_file(self) -> None:
		""" Will get the history of game scores from the file containing them.
		File is kept at the computer """
		self._game_results: List[GameResult] = self.manage_high_scores_file_helper.get_high_scores_from_file()
		return None
