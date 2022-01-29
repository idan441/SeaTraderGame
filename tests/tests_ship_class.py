import unittest
from classes.ship import Ship
from custom_exceptions.ship_custom_exceptions import CustomExceptionWrongVoyageTimeValueForShip


class TestShipClass(unittest.TestCase):
	def test_ship_upgrade(self):
		""" Test ship upgrade

		:return:
		"""
		ship_default_voyage_time = 10
		ship = Ship(voyage_time=ship_default_voyage_time,
					min_fix_cost_in_game=100,
					max_fix_cost_in_game=500,
					chance_for_ship_to_break=0.05)

		with self.assertRaises(expected_exception=CustomExceptionWrongVoyageTimeValueForShip):
			ship.upgrade_ship_voyage_time(ship_default_voyage_time + 1)

	def test_ship_break_event(self):
		""" Test a case where ship breaks in a break event
		( In game break chance is random, here it will be set to 100% )

		:return:
		"""
		ship_chance_to_break = 1  # =100% to break
		ship = Ship(voyage_time=1,
					min_fix_cost_in_game=100,
					max_fix_cost_in_game=500,
					chance_for_ship_to_break=ship_chance_to_break)

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
					chance_for_ship_to_break=ship_chance_to_break)

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
					chance_for_ship_to_break=1)
		ship.do_random_event_damage_ship()
		self.assertEqual(first=ship.is_ship_broken,
						 second=True,
						 msg="Ship's is_broken property needs to be True as it is broken!")


if __name__ == '__main__':
	unittest.main()
