from typing import List
from classes.products import Product

CITIES_LIST: List[str] = [
	"Yafo",
	"Larnaka",
	"Athena"
]
INITIAL_START_CITY = CITIES_LIST[0]

PRODUCTS_LIST: List[Product] = [
	Product(name="Wine", min_price=10, max_price=100),
	Product(name="Olives", min_price=10, max_price=100),
	Product(name="Flour", min_price=10, max_price=20),
]

INITIAL_BUDGET: int = 10000

# Game length time -
AMOUNT_OF_HOURS_FOR_WORKDAY: int = 16
TOTAL_TRADE_DAYS_IN_A_GAME: int = 3

# Player ship settings -
SHIP_TIME_TO_SAIL_BETWEEN_CITIES: int = 8
SHIP_UPGRADE_TIME_HOURS_REDUCTION: int = 2  # Amount of hours to reduce from the sail time ("voyage time") for every upgrade
SHIP_UPGRADE_PRICE: int = 1000  # Amount of budget to pay in order to upgrade the ship
SHIP_MINIMUM_FIX_COST_IN_GAME: int = 100
SHIP_MAXIMUM_FIX_COST_IN_GAME: int = 500
CHANCE_FOR_SHIP_TO_BREAK: float = 0.05  # Should be between 0 and 1

# High-scores file ( If doesn't exist - game will create one automatically )
GAME_HIGH_SCORES_FILE_PATH: str = "/tmp/sea_trader_high_scores.json"

# Logging file
GAME_LOGS_FILE_PATH: str = "/tmp/sear_trader_logs.txt"
