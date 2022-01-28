from typing import List, Optional, Dict
from input_handling.validators import ValidateUserInput
from custom_exceptions.validator_custom_exceptions import ValidationExceptionInputNotInOptionsList, \
	ValidationExceptionWrongNumericValue, ValidationExceptionInputNotNumeric, ValidateExceptionYesNoInputWrongValue

"""
UserInput class used to accept user input from terminal
"""


class UserInput:
	""" Used to get user input and validate it """

	def __init__(self):
		""""""
		pass

	@staticmethod
	def get_user_string_input(prompt_message: str, options_list: Optional[List[str]] = None) -> str:
		""" Will get a user string input from terminal.

		:param prompt_message: The question to ask the user before accepting the input
		:param options_list: Optional - a list of values which the input should be one of
		:return: input (str)
		"""
		while True:
			print(prompt_message, f"( Possible value: {options_list} )" if options_list is not None else "")
			try:
				if options_list is not None:
					user_input: str = ValidateUserInput.input_string_from_options_list(options_list=options_list)
				else:
					user_input: str = ValidateUserInput.input_string()
				return user_input
			except ValidationExceptionInputNotInOptionsList:
				print(f"Bad input. Value should be one of: {options_list}")

	@staticmethod
	def get_user_numeric_input(prompt_message: str,
							   options_list: Optional[List[int]] = None,
							   min_value: Optional[int] = None,
							   max_value: Optional[int] = None):
		""" Will get a user numeric input form terminal.
		Optional - specify a minimum or maximum value which the value should be between these

		:param prompt_message: The question to ask the user before accepting the input
		:param options_list: A list of possible values for the number ot be
		:param min_value: Min value for the number
		:param max_value: Max value for the number
		:return: input (num)
		"""
		while True:
			print(prompt_message, f"( Possible value: {options_list} )" if options_list is not None else "")
			try:
				user_input: int = ValidateUserInput.get_input_number(min_value=min_value, max_value=max_value)
				if options_list is not None:
					if user_input not in options_list:
						raise ValidationExceptionInputNotInOptionsList
				return user_input
			except ValidationExceptionWrongNumericValue:
				print(f"Bad input. Value should be "
					  f"{f'minimum {min_value}' if min_value is not None else ''} "
					  f"{'and' if min_value is not None and max_value is not None else ''} "
					  f"{f'maximum {max_value}' if max_value is not None else ''}")
			except ValidationExceptionInputNotNumeric:
				print(f"Bad input. Value needs to be numeric!")
			except ValidationExceptionInputNotInOptionsList:
				print(f"Bad input. Value should be one of: {options_list}")

	@staticmethod
	def get_user_number_input_for_menu(prompt_message: str, options_dict: Dict[int, str]) -> int:
		""" Will get a numeric option from a set of predefined numbers with option. This will also show a small
		description for each option. This is used by menus where player has multiple numeric options to choose.

		:param prompt_message: The question to ask the user before accepting the input
		:param options_dict: A dictionary (int, str) describing the options to choose - key should be the input number and
		                     value should be a description for the option
		:return: The selected option
		"""
		print(prompt_message)
		for key, value in options_dict.items():
			print(f"{key} - {value}")

		while True:
			print(f"Choose a number: ( Possible value: {options_dict.keys()} )")
			try:
				user_input: int = ValidateUserInput.input_int_from_options_list(options_list=[key for key in options_dict.keys()])
				return user_input
			except ValidationExceptionInputNotInOptionsList:
				print(f"Bad input. Value should be one of: {options_dict}")
			except ValidationExceptionInputNotNumeric:
				print(f"Bad input. Value needs to be numeric!")

	@staticmethod
	def get_user_yes_no_input(prompt_message: str) -> bool:
		""" Will get a yes/no input from the user and will return it as a boolean value.

		Currently supported input options: yes, no, Yes, No, y, n, Y, N

		:param prompt_message: The question to ask the user before accepting the input
		:return: Boolean
		"""
		accepted_yes_values: List[str] = ["y", "Y", "Yes", "yes"]
		accepted_no_values: List[str] = ["n", "N", "No", "no"]

		print(prompt_message, f"({accepted_yes_values[0]}/{accepted_no_values[0]})")
		while True:
			try:
				user_input: bool = ValidateUserInput.input_yes_no(accepted_yes_values=accepted_yes_values,
																  accepted_no_values=accepted_no_values)
				return user_input
			except ValidateExceptionYesNoInputWrongValue as e:
				print(e)
