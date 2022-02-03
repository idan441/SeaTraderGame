from pathlib import Path
from typing import List
from highscores.game_results import GameResults


"""
Contains functionality for managing the high scores table
"""


class ManageHighScoresFile:
	def __init__(self):
		self.high_scores_file_path: str = "/tmp/a"
		self.high_scores_file: Path = Path(self.high_scores_file_path)

	def is_high_scores_file_exist(self) -> bool:
		""" Checks if the high scores file exists

		:return: Boolean - true if file exists
		"""
		if self.high_scores_file.is_file():
			return True
		return False

	def read_high_scores_from_file(self) -> str:
		""" Will return the high scores file content

		:return: str
		"""
		file_content: str = self.high_scores_file.read_text()
		return file_content

	def update_high_scores_file(self):
		""""""
		pass

