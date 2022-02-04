from typing import List, Dict, Union
import json
from datetime import datetime
from pathlib import Path
from highscores.game_results import GameResult

"""
Contains functionality for managing the high scores table
"""


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
		self.high_scores_file_path: str = "/tmp/a"
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
		# TODO - add a check if the file exists + create it if it deosn't - in such case return an empty list ot the user as there areno game scores record
		file_content: str = self.high_scores_file.read_text()
		game_high_scores_as_json = json.loads(file_content)
		return game_high_scores_as_json

	def get_high_scores_from_file(self) -> List[GameResult]:
		""" Will return games high-scores data, based on the data file storing them

		:return: A list of game results, to be used by HighScores object
		"""
		game_high_scores_as_json = self.read_high_scores_data_from_file()
		games_results: List[GameResult] = []

		try:
			for game_result_details_in_json in game_high_scores_as_json:
				name: str = game_result_details_in_json["name"]
				coins_earned: int = game_result_details_in_json["coins_earned"]
				amount_of_trade_days: int = game_result_details_in_json["amount_of_trade_days"]
				game_datetime: datetime = game_result_details_in_json["game_datetime"]

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
		game_results_dict_formatted: List[Dict[str, any]] = []
		for game_result in game_results_list:
			game_results_dict_formatted.append(
				{
					"name": game_result.name,
					"coins_earned": game_result.coins_earned,
					"amount_of_trade_days": game_result.amount_of_trade_days,
					"game_datetime": game_result.game_datetime
				}
			)
		game_results_as_text_string: str = json.dumps(game_results_dict_formatted, indent=4, sort_keys=True, default=str)
		with self.high_scores_file.open("w", encoding="utf-8") as file:
			file.write(game_results_as_text_string)
		return None


class HighScores:
	""" Will manage the game's high score table """

	def __init__(self):
		"""

		"""
		self._game_results: List[GameResult] = []
		self.manage_high_scores_file_helper = ManageHighScoresFile()
		self.get_game_results_from_file()

	def load_game_results_from_json_text(self, game_results_as_json_text: str):
		""" Will take a JSON string containing games high-scores and will parse it to the class object

		:param game_results_as_json_text:
		:return: None
		"""

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
		return self._game_results

	def get_game_results_ordered_by_date(self) -> List[GameResult]:
		""" Will return game results ordered by date games played in ascending order

		:return: A list of all game results ordered by game dates
		"""
		return self._game_results

	def add_new_game_result(self, game_result: GameResult) -> None:
		""" Will add a game result to the high-scores

		:return: None
		"""
		self._game_results.append(game_result)

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
