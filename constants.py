from typing import List
from classes.products import Product

CITIES_LIST: List[str] = [
	"Yafo",
	"Larnaka",
	"Athena"
]

PRODUCTS_LIST: List[Product] = [
	Product(name="Wine", min_price=0, max_price=100),
	Product(name="Olives", min_price=10, max_price=100),
	Product(name="Flour", min_price=10, max_price=20),
]

INITIAL_BUDGET: int = 10000
AMOUNT_OF_HOURS_FOR_WORKDAY: int = 16
