from classes.game import Game
from input_handling.user_input import UserInput
from highscores.manage_high_scores_file import HighScores
from highscores.game_result import GameResult
from game_menus.manage_highscores_menu import HighScoresMenu
from game_menus.into_message import print_game_intro


def main():
	""" Will ask player for it's details and will start a game of Sea Trader

	:return:
	"""
	print_game_intro()

	game_high_scores = HighScores()
	high_scores_menu = HighScoresMenu(high_scores=game_high_scores)

	while True:
		menu_option_chosen: int = UserInput.get_user_number_input_for_menu(
			prompt_message="Choose an option from these: ",
			options_dict={
				1: "Introduction & instructions",
				2: "Start game",
				3: "High scores",
				4: "Exit",
			}
		)
		if menu_option_chosen == 1:
			print("You are a captain of a trading ship, raging the seven seas. "
				  "Your task is to get as many coins as you can after the trading season ends! "
				  "Good luck! ")
		elif menu_option_chosen == 2:
			player_name: str = UserInput.get_user_string_input(prompt_message="Please enter your name:",
															   is_none_allowed=False)
			game = Game(player_name=player_name)
			game.start_game()

			# Get game results - and save them
			game_result: GameResult = game.game_results
			game_high_scores.add_new_game_result(game_result=game_result)
		elif menu_option_chosen == 3:
			high_scores_menu.manage_high_scores_menu()
		elif menu_option_chosen == 4:
			break


if __name__ == "__main__":
	main()
