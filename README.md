# PostgreSQL Debezium Kafka MinIO Integration

This repository demonstrates an end-to-end data streaming pipeline using PostgreSQL, Debezium, Kafka, and MinIO. The pipeline captures real-time database changes, processes them through Kafka, and finally stores them in MinIO for further analysis.

For a detailed explanation and setup instructions, please refer to my Medium article:
[Real-Time End-to-End Data Streaming with PostgreSQL, Kafka, Minio, Prometheus, and Grafana](https://melbdataguy.medium.com/real-time-end-to-end-data-streaming-with-postgres-kafka-minio-prometheus-and-grafana-f0c4a4b6a792)


## Getting Started

1. Clone this repository:

   ```
   git clone https://github.com/your-username/postgres-debezium-kafka-s3.git
   cd postgres-debezium-kafka-s3
   ```

2. Follow the instructions in the Medium article to set up and configure PostgreSQL, Kafka, and S3.

3. Start the services using Docker Compose:

   ```
   docker-compose -f docker-compose-with-monitoring up -d
   ```

4. Monitor the pipeline and data flow using Prometheus and Grafana as described in the article.