
# Change Data Capture (CDC) Using Kafka, Debezium, and PostgreSQL

## Overview

This project demonstrates a **Change Data Capture (CDC)** pipeline to monitor and log changes in a PostgreSQL database. It tracks **when**, **where**, and **who** made changes to the data using the following tools:

- **Apache Kafka**: A distributed event streaming platform.
- **Zookeeper**: A centralized service for managing Kafka clusters.
- **Kafka Control Center**: A web-based interface to monitor and manage Kafka.
- **Debezium**: A CDC tool that streams database changes to Kafka topics.
- **PostgreSQL**: The relational database used for data storage.
- **Debezium UI**: A user interface to manage and monitor Debezium connectors.

The entire stack is deployed using Docker for simplicity and portability.

---

## Features

- **Real-time Change Monitoring**: Captures and streams changes in PostgreSQL data to Kafka topics.
- **Event Tracking**: Identifies the changes, including the time, affected table/field, and the user responsible for the change.
- **User-Friendly UI**: Manage Kafka topics and Debezium connectors using intuitive interfaces.
- **Scalable Architecture**: Uses Kafka to handle high-throughput event streaming.

---

## Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.
- Basic knowledge of Kafka, Debezium, and PostgreSQL.

---

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Start the Docker Environment**
   ```bash
   docker-compose up -d
   ```

3. **Verify the Services**
   - Kafka and Zookeeper are running.
   - Kafka Control Center is accessible at `http://localhost:<control_center_port>`.
   - Debezium UI is accessible at `http://localhost:<debezium_ui_port>`.

4. **Configure the PostgreSQL Database**
   - Set up a PostgreSQL database and enable logical replication.
   - Example:
     ```sql
     ALTER SYSTEM SET wal_level = 'logical';
     ALTER SYSTEM SET max_replication_slots = 10;
     ALTER SYSTEM SET max_wal_senders = 10;
     ```

5. **Set Up Debezium Connector**
   - Use the Debezium UI to create a connector for the PostgreSQL database.
   - Provide details such as:
     - Database host, port, username, password.
     - Tables to monitor for changes.

6. **Monitor Changes**
   - Changes in the PostgreSQL database are streamed to Kafka topics.
   - Use Kafka Control Center to view the Kafka topics and the corresponding data.
   - Identify the time, location, and user responsible for changes.

---

## Docker Services

| Service             | Description                                   | URL                           |
|---------------------|-----------------------------------------------|-------------------------------|
| **Kafka**           | Event streaming platform                     | N/A                           |
| **Zookeeper**       | Kafka cluster manager                        | N/A                           |
| **Kafka Control Center** | Kafka monitoring and management UI       | `http://localhost:<port>`     |
| **Debezium**        | Change Data Capture tool                     | N/A                           |
| **PostgreSQL**      | Relational database                          | `jdbc:postgresql://<host>:<port>/<db>` |
| **Debezium UI**     | Manage Debezium connectors                   | `http://localhost:<port>`     |

---

## Example Workflow

1. Insert, update, or delete a record in a PostgreSQL table.
2. Debezium captures the change and streams it to a Kafka topic.
3. The Kafka Control Center displays the events in real-time.
4. Information such as the timestamp, affected table/fields, and the user is logged.

---

## Sample docker-compose.yml

```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka
    depends_on:
      - zookeeper
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  control-center:
    image: confluentinc/cp-enterprise-control-center
    depends_on:
      - kafka
    environment:
      CONTROL_CENTER_BOOTSTRAP_SERVERS: kafka:9092
    ports:
      - "9021:9021"

  postgres:
    image: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: database
    ports:
      - "5432:5432"

  debezium-connect:
    image: debezium/connect
    depends_on:
      - kafka
    environment:
      BOOTSTRAP_SERVERS: kafka:9092
    ports:
      - "8083:8083"

  debezium-ui:
    image: debezium/debezium-ui
    ports:
      - "8084:8084"
```

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Feel free to customize the content further based on your specific project details or configurations!
