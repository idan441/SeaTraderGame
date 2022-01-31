from classes.game import Game
from input_handling.user_input import UserInput


def main():
	""" Will ask player for it's details and will start a game of Sea Trader

	:return:
	"""
	print("Welcome to Sea Trader game")
	print("Sea Trader is a homage to the famous game 'Socher HaYam'")

	while True:
		menu_option_chose: int = UserInput.get_user_number_input_for_menu(
			prompt_message="Choose an option from these: ",
			options_dict={
				1: "Introduction & instructions",
				2: "Start game",
				3: "High scores",
				4: "Credits",
				5: "Exit",
			}
		)
		if menu_option_chose == 1:
			print("You are a captain of a trading ship, raging the seven seas. "
				  "Your task is to get as many coins as you can after the trading season ends! "
				  "Good luck! ")
		elif menu_option_chose == 2:
			player_name: str = UserInput.get_user_string_input(prompt_message="Please enter your name:",
															   is_none_allowed=False)
			game = Game(player_name=player_name)
			game.start_game()
		elif menu_option_chose == 3:
			print("Here will be high scores table")
		elif menu_option_chose == 4:
			print("Programming: Idan")
		elif menu_option_chose == 5:
			break


if __name__ == "__main__":
	main()
