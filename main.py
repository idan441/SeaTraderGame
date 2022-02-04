from classes.game import Game
from input_handling.user_input import UserInput
from highscores.manage_high_scores_file import HighScores
from highscores.game_results import GameResult
from highscores.manage_highscores_menu import HighScoresMenu


def main():
	""" Will ask player for it's details and will start a game of Sea Trader

	:return:
	"""
	print("Welcome to Sea Trader game")
	print("Sea Trader is a homage to the famous game 'Socher HaYam'")
	print("""
	*******************************************
	*                                         *
	*          **        *          *         *
	*         * *      * *        * *         *
	*        *  *     *  *      * * *         *
	*       *   *    *   *          *         *
	*      *    *   *    *        * *         *
	*     * * * *  * * * *      * * *         *
	*           *        *          *         *
	*  *************************************  *
	*     ****  ****  ****  ****  ******      *
	*       **  ****  ****  ****  ****        *
	*        ************************         *
	*                                         *
	*******************************************
	
	""")

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
			game_result: GameResult = game.game_results
			print(game_result)
			game_high_scores.add_new_game_result(game_result=game_result)
			game_high_scores.update_game_results_file()
		elif menu_option_chosen == 3:
			high_scores_menu.manage_high_scores_menu()
		elif menu_option_chosen == 4:
			break


if __name__ == "__main__":
	main()
