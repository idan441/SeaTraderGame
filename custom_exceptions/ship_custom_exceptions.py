

"""
Custom exceptions related to Ship class
"""


class CustomExceptionWrongVoyageTimeValueForShip(Exception):
	""" Raises if trying to upgrade ship voyage time to a time bigger/equals than current ship voyage time. ( Voyage
	should lower the voyage time. ) """
