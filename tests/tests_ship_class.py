import unittest
from classes.ship import Ship
from custom_exceptions.ship_custom_exceptions import CustomExceptionWrongVoyageTimeValueForShip


class TestShipClass(unittest.TestCase):
	""" Will test Ship class """
	def test_ship_upgrade(self):
		""" Test ship upgrade which is supposed to fail due to 0 hours expected voyage time. ( Voyage time must be at
		least 1 hour! )

		:return:
		"""
		ship_default_voyage_time: int = 10
		ship_upgrade_time: int = 10
		ship = Ship(voyage_time=ship_default_voyage_time,
					min_fix_cost_in_game=100,
					max_fix_cost_in_game=500,
					chance_for_ship_to_break=0.05,
					ship_upgrade_time_by_hours=ship_upgrade_time)

		self.assertFalse(expr=ship.is_ship_upgradeable(), msg="Ship is not supposed to be upgradeable as the new "
															  "voyage will be 0 hours! ")
		with self.assertRaises(expected_exception=CustomExceptionWrongVoyageTimeValueForShip):
			ship.upgrade_ship_voyage_time()

	def test_ship_upgrade_time_success(self):
		""" Test a ship upgrade which is expected to succeed

		:return:
		"""
		ship_default_voyage_time: int = 10
		ship_upgrade_time: int = 4
		ship_expected_voyage_time_after_first_upgrade: int = ship_default_voyage_time - ship_upgrade_time
		ship_expected_voyage_time_after_second_upgrade: int = \
			ship_expected_voyage_time_after_first_upgrade - ship_upgrade_time

		ship = Ship(voyage_time=ship_default_voyage_time,
					min_fix_cost_in_game=100,
					max_fix_cost_in_game=500,
					chance_for_ship_to_break=0.05,
					ship_upgrade_time_by_hours=ship_upgrade_time)

		# Check ship is upgradeable and upgrade it for first time - expected voyage time should be 6 hours
		self.assertTrue(expr=ship.is_ship_upgradeable(), msg="Ship is supposed to be upgradeable! ")
		self.assertIsNone(obj=ship.upgrade_ship_voyage_time(), msg="Upgrade supposed to succeed 3rd time!")
		self.assertEqual(first=ship_expected_voyage_time_after_first_upgrade,
						 second=ship.voyage_time,
						 msg=f"Expected voyage time is supposed to be {ship_expected_voyage_time_after_first_upgrade}")

		# Check ship is upgradeable and upgrade it for first time - expected voyage time should be 6 hours
		self.assertTrue(expr=ship.is_ship_upgradeable(), msg="Ship is supposed to be upgradeable! ")
		self.assertIsNone(obj=ship.upgrade_ship_voyage_time(), msg="Upgrade supposed to succeed for 2nd time!")
		self.assertEqual(first=ship_expected_voyage_time_after_second_upgrade,
						 second=ship.voyage_time,
						 msg=f"Expected voyage time is supposed to be {ship_expected_voyage_time_after_second_upgrade}")

		# Now voyage time is supposed to be 2 - and upgrading it by upgradingit again is should to raise an exception!
		self.assertFalse(expr=ship.is_ship_upgradeable(), msg="Ship is not supposed to be upgradeable! ")
		with self.assertRaises(expected_exception=CustomExceptionWrongVoyageTimeValueForShip):
			ship.upgrade_ship_voyage_time()

	def test_ship_break_event(self):
		""" Test a case where ship breaks in a break event
		( In game break chance is random, here it will be set to 100% )

		:return:
		"""
		ship_chance_to_break = 1  # =100% to break
		ship = Ship(voyage_time=1,
					min_fix_cost_in_game=100,
					max_fix_cost_in_game=500,
					chance_for_ship_to_break=ship_chance_to_break,
					ship_upgrade_time_by_hours=2)

		is_ship_broken: bool = ship.do_random_event_damage_ship()
		self.assertTrue(expr=is_ship_broken,
						msg="Ship is support to be broken!")


	def test_ship_not_break_event(self):
		""" Test a case where ship doesn't break in a break event
		 ( In game break chance is random, here it will be set to 0% so ship will not break)

		:return:
		"""
		ship_chance_to_break = 0  # =0% to break
		ship = Ship(voyage_time=1,
					min_fix_cost_in_game=100,
					max_fix_cost_in_game=500,
					chance_for_ship_to_break=ship_chance_to_break,
					ship_upgrade_time_by_hours=2)

		is_ship_broken: bool = ship.do_random_event_damage_ship()
		self.assertFalse(expr=is_ship_broken,
						 msg="Ship should not be broken!")

	def test_is_ship_broken(self):
		""" Checks if a ship object, which has been broken - will have it's is_broken property is set to True

		:return:
		"""
		ship = Ship(voyage_time=1,
					min_fix_cost_in_game=100,
					max_fix_cost_in_game=500,
					chance_for_ship_to_break=1,
					ship_upgrade_time_by_hours=2)
		ship.do_random_event_damage_ship()
		self.assertEqual(first=ship.is_ship_broken,
						 second=True,
						 msg="Ship's is_broken property needs to be True as it is broken!")


if __name__ == '__main__':
	unittest.main()
