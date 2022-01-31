from typing import List, Union


"""
Includes methods for formatting text to nice output strings. The formatted output will be shown to the player
"""


class FormatOutput:
	""" Used to format string, lists etc.. to nice string to be shown as a user output. ( User = player in game ) """
	@staticmethod
	def return_options_list_as_string(options_list: List[Union[int, str]]) -> str:
		""" Will take a list and will return a str with all items comma separated

		This is used by get_user_number_input_for_menu() in order to show the user a nicer output

		Example - [1, 2, 3, 99] -> "1, 2, 3, 99"

		:param options_list:
		:return: A string with the options_list values comma separated
		"""
		options_list_str_formatted: List[str] = [str(option) for option in options_list]
		return ", ".join(options_list_str_formatted)
