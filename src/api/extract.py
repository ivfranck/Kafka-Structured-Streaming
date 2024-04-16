import traceback
from logging import Logger
from typing import Any

import requests
from pprint import pprint
from src.constants import API_URL


class CoinGeckoAPI:
    def __init__(self, checkpoint: str, logger: Logger = None):
        """
        :param checkpoint: The checkpoint identifier(datetime).
        :param logger: The logger object for logging events. Defaults to None.
        """
        self.checkpoint = checkpoint
        self.logger = logger

    def get_coin_data(self) -> list[dict[str, Any]]:
        """
        Fetches cryptocurrency data from CoinGecko API and processes it into a structured format.

        This method sends a GET request to the API, processes the JSON response, and constructs a list of dictionaries,
        each representing a cryptocurrency with its various attributes.

        :return: list[dict[str, Any]]: A list of dictionaries containing coin data.
        """
        global data
        try:
            self.logger.info(f"Fetching data from endpoint: {API_URL}")
            request = requests.get(API_URL)
            payload = request.json()

            data = []

            for coin in payload:
                data.append({
                    'id': coin['id'],
                    'symbol': coin['symbol'],
                    'name': coin['name'],
                    'image': coin['image'],
                    'current_price': coin['current_price'],
                    'market_cap': coin['market_cap'],
                    'market_cap_rank': coin['market_cap_rank'],
                    'fully_diluted_valuation': coin['fully_diluted_valuation'],
                    'total_volume': coin['total_volume'],
                    'high_24h': coin['high_24h'],
                    'low_24h': coin['low_24h'],
                    'price_change_24h': coin['price_change_24h'],
                    'price_change_percentage_24h': coin['price_change_percentage_24h'],
                    'market_cap_change_24h': coin['market_cap_change_24h'],
                    'market_cap_change_percentage_24h': coin['market_cap_change_percentage_24h'],
                    'circulating_supply': coin['circulating_supply'],
                    'total_supply': coin['total_supply'],
                    'max_supply': coin['max_supply'],
                    'ath': coin['ath'],
                    'ath_change_percentage': coin['ath_change_percentage'],
                    'ath_date': coin['ath_date'],
                    'atl': coin['atl'],
                    'atl_change_percentage': coin['atl_change_percentage'],
                    'atl_date': coin['atl_date'],
                    'last_updated': coin['last_updated'],
                    'checkpoint': self.checkpoint
                })
            self.logger.info(f"{len(data)} coins fetched")
        except:
            self.logger.error(traceback.format_exc())

        return data

