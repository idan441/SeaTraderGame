

"""
Defines custom exception for the UserInput class defined at ./classes/validator.py file
"""


class ValidationExceptionWrongNumericValue(Exception):
	""" Raises when a numeric input is bigger/smaller than needed. """
	pass


class ValidationExceptionInputNotNumeric(Exception):
	""" Raises when a numeric input given is not a numeric. ( = value fails to be casted to integer ) """
	pass


class ValidationExceptionInputNotInOptionsList(Exception):
	""" Raises when a string input is not in given list of options it can be one of. """
	pass
