from typing import List


"""
Will hold objects used for validating inputs of users + input of values in game
"""


class UserInput:
	""" Used to get user input from terminal and validate """
	@staticmethod
	def input_number() -> int:
		"""

		:return:
		"""

		pass

	@staticmethod
	def input_options(options_list: List[str]) -> str:
		"""

		:param options_list:
		:return:
		"""

		pass

	@staticmethod
	def is_number_in_range(min_value: int, max_value: int) -> int:
		"""

		:param min_value:
		:param max_value:
		:return:
		"""

		pass

	@staticmethod
	def get_user_input() -> str:
		""" Will get input from the user's terminal

		:return: un-validated user input
		"""
		user_input: str = input()
		return user_input
