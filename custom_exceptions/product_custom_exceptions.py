

"""
Contains custom exceptions used by all products related class objects
"""


class CustomExceptionProductDoesNotExists(Exception):
	""" Raises when trying to search or use a product which doesn't exist in game """
	pass


class CustomExceptionPlayerHasNotEnoughBudget(Exception):
	""" Raises when trying to sub from player's budget below zero.
	Such a case can happen in case player tries to buy more than he can pay for. """