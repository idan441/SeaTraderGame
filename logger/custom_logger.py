import logging
import json
from constants import GAME_LOGS_FILE_PATH

"""
Defines a logger configurations for the game
"""


def configure_logger():
	""" Will configure the logging module to use a JSON customized logging

	:return: None
	"""
	logger_format: str = json.dumps(
		{
			"module_name": "%(name)s",
			"date": "%(asctime)s",
			"log_level": "%(levelname)s",
			"message": "%(message)s"
		}
	)

	logging.basicConfig(
		filename=GAME_LOGS_FILE_PATH,
		format=logger_format,
		level=logging.INFO,
		datefmt="%Y-%m-%d %H:%M:%S",
	)

	return None
