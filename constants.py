from typing import List
from classes.products import Product

CITIES_LIST: List[str] = [
	"Yafo",
	"Larnaka",
	"Athena"
]
INITIAL_START_CITY = CITIES_LIST[0]

PRODUCTS_LIST: List[Product] = [
	Product(name="Wine", min_price=0, max_price=100),
	Product(name="Olives", min_price=10, max_price=100),
	Product(name="Flour", min_price=10, max_price=20),
]

INITIAL_BUDGET: int = 10000

AMOUNT_OF_HOURS_FOR_WORKDAY: int = 16
TIME_TO_SAIL_BETWEEN_CITIES: int = 8
TOTAL_TRADE_DAYS_IN_A_GAME: int = 3