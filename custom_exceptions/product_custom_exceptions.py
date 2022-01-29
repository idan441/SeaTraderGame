

"""
Contains custom exceptions used by all products related class objects
"""


# Exceptions when trying to create a product with wrong values
class CustomExceptionProductMinPriceIsBiggerThanMaxPrice(Exception):
	""" Raises when trying to create a product with a minimum price bigger than maximum price """
	pass


class CustomExceptionProductHasEmptyName(Exception):
	""" Raises when trying to create a product with an empty name """
	pass


class CustomExceptionProductDoesNotExists(Exception):
	""" Raises when trying to search or use a product which doesn't exist in game """
	pass


class CustomExceptionPlayerHasNotEnoughBudget(Exception):
	""" Raises when trying to sub from player's budget below zero.
	Such a case can happen in case player tries to buy more than he can pay for. """


class CustomExceptionsTransactionFailNotEnoughItemAmount(Exception):
	""" Raises when trying to do a sell transaction, and the player has not enough of the item to sell in his
	inventory """
