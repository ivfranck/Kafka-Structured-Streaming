from logging import Logger

from pyspark.sql.functions import from_json, col, DataFrame
from cassandra.cluster import Cluster

from config.spark import spark
from src.utils.schema import schema


class SparkStream:

    def __init__(self, checkpoint: str, logger: Logger = None):
        """
        :param checkpoint: A string representing a checkpoint for the data streaming process.
        :param logger: A logger instance for logging information and errors. Defaults to None.
        """
        self.checkpoint = checkpoint
        self.logger = logger

    def read_kafka_stream(self) -> DataFrame:
        """
        Reads data from a Kafka topic into a Spark DataFrame.

        This method configures a Spark streaming source to read from 'crypto_coins' Kafka topic,
        deserializes the messages, and filters them based on a checkpoint value (datetime).

        :return: A Spark DataFrame containing the filtered data from the Kafka topic.
        """
        self.logger.info("Reading Kafka Stream...")

        stream_df = (
            spark
            .readStream
            .format('kafka')
            .option('kafka.bootstrap.servers', 'localhost:9092')
            .option('subscribe', 'crypto_coins')
            .option('startingOffsets', 'earliest')
            .load()
        )

        sel = stream_df.selectExpr("CAST(value AS STRING)") \
            .select(from_json(col('value'), schema).alias('data')).select("data.*")

        last_checkpoint = sel.select("*").where(col("checkpoint") == self.checkpoint)

        # streaming_query = (last_checkpoint.writeStream.format("console")
        #                    .start())
        #
        # streaming_query.awaitTermination()

        return last_checkpoint

    def cassandra_connection(self):
        """
        Establishes a connection to a Cassandra cluster.

        :return: A connection to the Cassandra cluster if successful, otherwise None.
        """
        try:
            # connect to cassandra cluster
            cluster = Cluster(['localhost'])

            conn = cluster.connect()
            self.logger.info("Successfully connected to cassandra!")
            return conn
        except Exception as e:
            self.logger.error(f"Could not create cassandra connection due to {e}")
            return None

    def create_keyspace(self, conn):
        """
        Creates a keyspace in Cassandra if it does not already exist.

        :param conn: A connection to the Cassandra cluster.
        """
        conn.execute("""CREATE KEYSPACE IF NOT EXISTS crypto WITH REPLICATION = { 'class' : 'SimpleStrategy', 
        'replication_factor' : '1' };""")

        self.logger.info("Keyspace created successfully!")

    def create_cassandra_table(self, conn):
        """
        Creates a table in Cassandra if it does not already exist.

        :param conn: A connection to the Cassandra cluster.
        """
        conn.execute("""
            CREATE TABLE IF NOT EXISTS crypto.coins (
            id VARCHAR PRIMARY KEY,
            symbol VARCHAR,
            name VARCHAR,
            image VARCHAR,
            current_price DOUBLE,
            market_cap BIGINT,
            market_cap_rank INT,
            fully_diluted_valuation VARCHAR,
            total_volume BIGINT,
            high_24h DOUBLE,
            low_24h DOUBLE,
            price_change_24h DOUBLE,
            price_change_percentage_24h DOUBLE,
            market_cap_change_24h DOUBLE,
            market_cap_change_percentage_24h DOUBLE,
            circulating_supply DOUBLE,
            total_supply VARCHAR,
            max_supply VARCHAR,
            ath DOUBLE,
            ath_change_percentage DOUBLE,
            ath_date VARCHAR,
            atl DOUBLE,
            atl_change_percentage DOUBLE,
            atl_date VARCHAR,
            last_updated VARCHAR,
            checkpoint VARCHAR
                );
            """)

        self.logger.info("Table created successfully!")

    def write_to_cassandra(self, df: DataFrame, keyspace: str, table: str):
        """
        Writes data from a Spark DataFrame to a Cassandra table.

        :param df: The Spark DataFrame containing the data to be written.
        :param keyspace: The name of the Cassandra keyspace.
        :param table: The name of the Cassandra table.

        :return: True if the write operation was successful, otherwise False.
        """
        query = (df.writeStream
                 .format("org.apache.spark.sql.cassandra")
                 .outputMode("append")
                 .option("checkpointLocation", "/tmp/cassandra/")
                 .options(table=table, keyspace=keyspace)
                 .start())

        return query.awaitTermination()

    def start_stream(self):
        """
        Starts the streaming process by connecting to Cassandra, creating necessary keyspace and table,
        and writing data from Kafka to Cassandra.
        """
        cassandra_conn = self.cassandra_connection()

        if cassandra_conn:
            keyspace = self.create_keyspace(cassandra_conn)
            table = self.create_cassandra_table(cassandra_conn)
            self.write_to_cassandra(self.read_kafka_stream(), 'crypto', 'coins')
