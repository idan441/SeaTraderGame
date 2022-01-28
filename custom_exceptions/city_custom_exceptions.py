

"""
Defines custom exceptions for city classes
"""


class CustomExceptionCityNameNotFound(Exception):
	""" Raises when trying to query by name for a city which doesn't exist """
	pass
