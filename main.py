from classes.game import Game


def main():
	""" Will ask player for it's details and will start a game of Sea Trader

	"""
	print("Welcome to Sea Trader game")
	print("Sea Trader is a homage to Socher HaYam")

	print("Please enter your name:")
	player_name: str = input()
	game = Game(player_name=player_name)
	game.start_game()


if __name__ == "__main__":
	main()
