

"""
File has a nice ASCII art for the intro of the game.
The methods in this file are used solely by main.py file
"""


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
