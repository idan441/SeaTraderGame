from typing import List, Optional
from custom_exceptions.validator_custom_exceptions import ValidationExceptionWrongNumericValue, \
	ValidationExceptionInputNotNumeric, ValidationExceptionInputNotInOptionsList

"""
Will hold objects used for validating inputs of users + input of values in game
"""


class UserInput:
	""" Used to get user input from terminal and validate """
	@staticmethod
	def get_input_number(min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
		""" Will get numeric input from user.

		Optional - a min or max value can be specified

		:return: input as number (int) , in case input is illegal - an exception will be thrown
		"""
		try:
			input_casted_to_int: int = int(input())
		except ValueError:
			raise ValidationExceptionInputNotNumeric("Wrong input - input not numeric!")
		if min_value is not None:
			if input_casted_to_int < min_value:
				raise ValidationExceptionWrongNumericValue(f"Value should be smaller/equals than {min_value}")
		if max_value is not None:
			if input_casted_to_int > max_value:
				raise ValidationExceptionWrongNumericValue(f"Value should be bigger/equals than {max_value}")
		return input_casted_to_int

	@staticmethod
	def input_string_from_options_list(options_list: List[str]) -> str:
		""" Checks if a string input is one of the given options

		:param options_list: A list of options (str) which can be the input
		:return: input (str) , in case the input is not one of the options - an exception will raise
		"""
		input_value: str = input()
		if input_value in options_list:
			return input_value
		else:
			raise ValidationExceptionInputNotInOptionsList(f"Input given {input_value} "
														   f"is not in the options list: {options_list}")
