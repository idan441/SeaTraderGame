import logging


logger = logging.getLogger(__name__)


"""
File has a nice ASCII art for the intro of the game.
The methods in this file are used solely by main.py file
"""


def print_game_intro() -> None:
	""" Will print a nice ship ASCII art to the terminal session

	:return: None
	"""
	print("Welcome to Sea Trader game")
	print("Sea Trader is a homage to the famous game 'Socher HaYam' by Matach")
	print_ship_art()
	print("You are a captain of a trading ship, raging the seven seas.\n"
		  "Your task is to get as many coins as you can after the trading season ends!\n"
		  "Good luck!\n")
	logger.debug("Game started - printed intro message")
	return None


def print_ship_art() -> None:
	""" Will print a nice ship ASCII art to the terminal session

	:return: None
	"""
	ship_art: str = """
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
	"""
	print(ship_art)
	return None
