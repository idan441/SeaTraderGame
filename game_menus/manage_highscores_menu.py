from typing import List, Dict
from tabulate import tabulate
from highscores.manage_high_scores_file import HighScores
from highscores.game_result import GameResult
from input_handling.user_input import UserInput


"""
Manages game menus for high scores
"""


class HighScoresMenu:
	""" Will print menus for the game high scores """
	def __init__(self, high_scores: HighScores):
		"""

		"""
		self.high_scores: HighScores = high_scores

	def manage_high_scores_menu(self) -> None:
		""" Will manage the high scores menu

		:return: None
		"""
		print("High scores menu")
		while True:
			option_chosen: int = UserInput.get_user_number_input_for_menu(
				prompt_message="Choose an option: ",
				options_dict={
					1: "Show top high scores by amount of cash",
					2: "Show top high scores by date",
					3: "Reset high scores",
					4: "Back to former menu",
				}
			)

			if option_chosen == 1:
				self.print_game_high_scores_ordered_by_amount_of_cash()
			elif option_chosen == 2:
				self.print_game_high_scores_ordered_by_date()
			elif option_chosen == 3:
				print("To add")
			elif option_chosen == 4:
				break
		return None

	def print_game_high_scores_ordered_by_amount_of_cash(self) -> None:
		""" Will print the game scores history, ordered by amount of cash the player scored in ascending order

		:return: None
		"""
		self.print_games_high_score_table_formatted(
			game_results_list=self.high_scores.get_game_results_ordered_by_score()
		)
		return None

	def print_game_high_scores_ordered_by_date(self) -> None:
		""" Will print the game scores history, ordered by game date in ascending order

		:return: None
		"""
		self.print_games_high_score_table_formatted(
			game_results_list=self.high_scores.get_game_results_ordered_by_date()
		)
		return None

	@staticmethod
	def print_games_high_score_table_formatted(game_results_list: List[GameResult]) -> None:
		""" Will print the game high scores table to the terminal formatted

		:return: None
		"""
		game_results: List[Dict] = [game_result.get_game_result_as_dict() for game_result in game_results_list]
		print(tabulate(tabular_data=game_results, headers="keys"))

		return None
