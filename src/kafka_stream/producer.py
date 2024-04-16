import json
from logging import Logger
from typing import Any

from kafka import KafkaProducer


class KafkaProducerHandler:
    def __init__(self, logger: Logger = None):
        """
        :param logger: A logger instance for logging information and errors. Defaults to None.
        """
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        self.logger = logger

    def push_to_queue(self, data: dict[str, Any], key: str):
        """
        Sends a message to a Kafka topic.

        This method serializes the provided data dictionary into a JSON string, encodes it as UTF-8, and sends it to
        the 'crypto_coins' Kafka topic. It also encodes the key as UTF-8 and sends it along with the message.

        :param data: The data to be sent as a message to the Kafka topic.
        :param key: The key to be used for partitioning the message in the Kafka topic.
        """
        self.producer.send('crypto_coins', json.dumps(data).encode('utf-8'), key=key.encode('utf-8'))
        self.producer.flush()
