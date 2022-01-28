

"""
Contains custom exceptions used by all products related class objects
"""


class CustomExceptionProductDoesNotExists(Exception):
	""" Raises when trying to search or use a product which doesn't exist in game """
	pass
