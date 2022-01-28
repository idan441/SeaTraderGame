from classes.game import Game
from input_handling.user_input import UserInput


def main():
	""" Will ask player for it's details and will start a game of Sea Trader

	"""
	print("Welcome to Sea Trader game")
	print("Sea Trader is a homage to Socher HaYam")

	while True:
		menu_option_chose: int = UserInput.get_user_number_input_for_menu(
			prompt_message="Choose an option from these: ",
			options_dict={
				1: "Start game",
				2: "High scores",
				3: "Credits",
				4: "Exit",
			}
		)

		if menu_option_chose == 1:
			player_name: str = UserInput.get_user_string_input(prompt_message="Please enter your name:")
			game = Game(player_name=player_name)
			game.start_game()
		elif menu_option_chose == 2:
			print("Here will be high scores table")
		elif menu_option_chose == 3:
			print("Programming Idan")
		elif menu_option_chose == 4:
			break


if __name__ == "__main__":
	main()
