import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))

API_URL = config.get('coingecko', 'API_URL')