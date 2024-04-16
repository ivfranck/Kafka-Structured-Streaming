# Kafka-Structured-Streaming

---
## Overview

---
This project demonstrates the integration of Kafka, Spark Streaming, and Cassandra all containerized with Docker to create a scalable and efficient data processing pipeline. 
The workflow involves reading messages from Kafka, processing them with Spark Streaming, and then storing the processed data in Cassandra. 
This setup is particularly useful for real-time data analytics and processing.
## System Architecture

---
![Preview Storage](System%20Architecture.png)
## Project Structure

---
The project is divided into three main components:
- `src/api`: A Python script that fetches cryptocurrency data from the CoinGecko API and processes it into a structured format.
- `src/kafka_stream`: A Python script that includes code related to the Kafka producer responsible for pushing data into the Kafka topic.
- `src/spark_cassandra_stream`: A Python script that includes the Spark Streaming code. This component is responsible for reading messages from Kafka, processing them, and writing the results to Cassandra.

## Getting Started

---
### Docker Compose Setup
This project utilizes Docker Compose to manage the services required for the application. The `docker-compose.yml` file 
defines the services for Kafka, Zookeeper, Schema Registry, Control Center, KSQLDB Server, Spark Master and Worker, and Cassandra. To start the services, run:
```
docker-compose up -d

```
This command will start all the services defined in the docker-compose.yml file in detached mode. Ensure Docker and Docker Compose are installed on your machine and opened before running this command.

Once all services are up and running, run the [run.py ](src/run.py)  file to start the streaming.

To view the data in cassandra, simply run the following command in the terminal to access the cqlsh cli:

```
!curl docker exec -it cassandra cqlsh -u cassandra -p cassandra localhost 9042
```
## Sources

---
### Docker Compose Kafka
https://docs.confluent.io/platform/current/installation/docker/image-reference.html

https://www.baeldung.com/ops/kafka-docker-setup

https://hub.docker.com/_/zookeeper

### Spark
https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html

### Cassandra
https://cassandra.apache.org/_/quickstart.html