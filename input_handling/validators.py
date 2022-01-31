from typing import List, Optional
from custom_exceptions.validator_custom_exceptions import ValidationExceptionWrongNumericValue, \
	ValidationExceptionInputNotNumeric, ValidationExceptionInputNotInOptionsList, \
	ValidateExceptionYesNoInputWrongValue, ValidateExceptionInputIsEmpty
from input_handling.text_formatter import FormatOutput


"""
Will hold objects used for validating inputs of users + input of values in game
"""


class ValidateUserInput:
	""" A collection of static methods used for validating values which are accepted by user input """
	@staticmethod
	def get_input_number(min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
		""" Accepts input from user. Will get numeric input from user.

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
	def input_string(is_none_allowed: bool = False) -> str:
		""" Accepts input from user. Returns the input as a string without any validation.

		:param is_none_allowed: Optional - can a null string be accepted, default: False
		:return: input (str) , in case is_none_allows=True and input is empty - an exception will be raised
		"""
		input_value: str = input()
		if not is_none_allowed and input_value == "":
			raise ValidateExceptionInputIsEmpty("Input value must not be null!")
		return input_value

	@staticmethod
	def input_string_from_options_list(options_list: List[str]) -> str:
		""" Accepts input from user. Checks if a string input is one of the given options

		:param options_list: A list of options (str) which can be the input
		:return: input (str) , in case the input is not one of the options - an exception will raise
		"""
		input_value: str = input()
		if input_value in options_list:
			return input_value
		else:
			raise ValidationExceptionInputNotInOptionsList(f"Input given {input_value} "
														   f"is not in the options list: {options_list}")

	@staticmethod
	def input_int_from_options_list(options_list: List[int]) -> int:
		""" Accepts input from user. Checks if a int input is one of the given options

		:param options_list: A list of options (int) which can be the input
		:return: input (int) , in case the input is not one of the options - an exception will raise
		"""
		input_value: int = ValidateUserInput.get_input_number()
		if input_value in options_list:
			return input_value
		else:
			raise ValidationExceptionInputNotInOptionsList(f"Input given {input_value} "
														   f"is not in the options list: {options_list}")

	@staticmethod
	def input_yes_no(accepted_yes_values: List[str], accepted_no_values: List[str]) -> bool:
		""" Accepts input from user. Will get a yes/no input from the user and will return it as a boolean value.

		:param accepted_yes_value: A list of value which will be accepted as yes
		:param accepted_no_value: A list of value which will be accepted as no
		:return: Boolean - true in case input is in the accepted yes list of values, false in case input is in the
						   accepted no list of values.
						   In case value is different from both lists - an exception will raise
		"""
		input_value: str = input()
		if input_value in accepted_yes_values:
			return True
		elif input_value in accepted_no_values:
			return False
		else:
			accepted_values: str = FormatOutput.return_options_list_as_string(
				options_list=accepted_yes_values + accepted_no_values
			)
			raise ValidateExceptionYesNoInputWrongValue(f"Wrong value given for yes/no - "
														f"possible values: {accepted_values})")
