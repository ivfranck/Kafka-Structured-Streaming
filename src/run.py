import datetime
import traceback

from config.logging_conf import LOGGER
from config.spark import spark
from api.extract import CoinGeckoAPI
from kafka_stream.producer import KafkaProducerHandler
from src.spark_cassandra_stream.spark_streaming import SparkStream

if __name__ == '__main__':
    """
    Main entry point for the script.

    This script fetches cryptocurrency data from CoinGecko API, pushes it to a Kafka stream, and then starts a Spark 
    stream to process the data."""

    checkpoint = datetime.datetime.now().isoformat()
    LOGGER.info(f"Checkpoint: {checkpoint}")

    api_data = CoinGeckoAPI(checkpoint, LOGGER).get_coin_data()

    coin_count = 0
    try:
        for coin in api_data:
            key = coin['id']
            KafkaProducerHandler(LOGGER).push_to_queue(coin, key)
            coin_count += 1
        LOGGER.info(f"{coin_count} coins pushed to kafka stream successfully!")
    except:
        LOGGER.error(traceback.format_exc())

    SparkStream(checkpoint, LOGGER).start_stream()
    spark.stop()

