import unittest
from classes.player import Player
from custom_exceptions.product_custom_exceptions import CustomExceptionPlayerHasNotEnoughBudget


"""
Tests for player class
"""


class TestPlayer(unittest.TestCase):
	""" Tests for Player object """
	def test_create_a_player_objects(self):
		""" Will try to create a Player object

		:return:
		"""
		Player(name="dummy_name", initial_budget=0, initial_location="Yafo")

	def test_add_and_remove_budget(self):
		""" Will try to create a player and then will try to add and remove budget from the player

		:return:
		"""
		initial_budget: int = 0
		budget_to_add: int = 100
		budget_to_remove: int = 80
		final_budget: int = 20

		player = Player(name="dummy_name", initial_budget=initial_budget, initial_location="Yafo")
		player.add_budget(budget_to_add)
		self.assertEqual(first=budget_to_add, second=player.budget)
		player.sub_budget(budget_to_remove)
		self.assertEqual(first=final_budget, second=player.budget)

		# Check the budget is not the initla or middle budgets
		self.assertNotEqual(first=player.budget, second=initial_budget)
		self.assertNotEqual(first=player.budget, second=budget_to_add)
		self.assertNotEqual(first=player.budget, second=budget_to_remove)

	def test_remove_budget_from_player_when_he_has_not_enough(self):
		""" Will try to remove budget from a player who is having not enough budget

		:return:
		"""
		initial_budget: int = 0
		budget_to_remove: int = 10
		player = Player(name="dummy_name", initial_budget=initial_budget, initial_location="Yafo")

		with self.assertRaises(CustomExceptionPlayerHasNotEnoughBudget):
			player.sub_budget(budget_to_remove=budget_to_remove)

	def test_change_player_city_location(self):
		""" Test changing player's city location

		:return:
		"""
		initial_location: str = "Yafo"
		new_location: str = "Haifa"
		player = Player(name="dummy_name", initial_budget=0, initial_location=initial_location)
		player.location = new_location
		self.assertEqual(first=player.location, second=new_location)
		self.assertNotEqual(first=player.location, second=initial_location)
