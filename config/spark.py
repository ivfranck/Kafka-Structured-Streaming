from pyspark.sql import SparkSession

# spark setup
spark = (
    SparkSession
    .builder
    .appName("crypto-analytics")
    .config('spark.jars.packages', "com.datastax.spark:spark-cassandra-connector_2.12:3.5.0,"
                                   "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1"
            )
    .config("spark.sql.repl.eagerEval.enabled", True)
    .getOrCreate()
)
