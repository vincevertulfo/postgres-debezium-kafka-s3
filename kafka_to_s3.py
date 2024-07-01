# from kafka import KafkaConsumer
from confluent_kafka import Consumer
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import MessageField, SerializationContext
import json
from datetime import datetime
import os
import boto3

# Credentials and Connection Info
access_key = "minio"
secret_key = "minio123"
endpoint = "http://localhost:9000"  # MinIO endpoint
region = "us-east-1"

# Create a session using the access key and secret key
session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
)

# Create an S3 client with MinIO endpoint
s3 = session.client('s3',
                    endpoint_url=endpoint,
                    region_name=region,
                    # config=Config(signature_version='s3v4'), if required
                   )
# Get schema str
schema_registry_url = "http://localhost:8085" 
schema_registry_client = SchemaRegistryClient({"url":schema_registry_url })
schema_version = schema_registry_client.get_latest_version(
    'postgres.public.ingredients-value'
)
schema_id = schema_version.schema_id
schema = schema_registry_client.get_schema(schema_id)
schema_str = schema.schema_str

avro_deserializer = AvroDeserializer(schema_registry_client, schema_str)

# Configure the Kafka consumer
consumer = Consumer(
            {"bootstrap.servers": "localhost:29092", "group.id": 'group-1'}
        )

consumer.subscribe(['postgres.public.ingredients'])

# Continuously poll for new messages
print("Listening..")
try:
    while True:

        msg = consumer.poll(1.0)
        print(msg)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        byte_message = msg.value()
        if byte_message is None:
            print("Received tombstone message, skipping...")
            continue
        
        print(
            f"Byte message: {byte_message}, Type: {type(byte_message)}"
        )
        decoded_message = avro_deserializer(
                    byte_message, SerializationContext(['postgres.public.ingredients'], MessageField.VALUE)
                )

        print(
            f"Decoded message: {decoded_message}, Type: {type(decoded_message)}"  # noqa: E501
        )
        
        # Convert dictionary to JSON string
        json_data = json.dumps(decoded_message)

        # Upload JSON data as an object to MinIO
        bucket_name = 'ingredients'  # Replace with your MinIO bucket name
        
        # Get current date and time
        current_datetime = datetime.now()
                
        # Format current date in YYYY-MM-DD format
        current_date = current_datetime.strftime("%Y-%m-%d")

        # Format current time in HH-MM-SS format
        current_time = current_datetime.strftime("%H-%M-%S")

        # Example object key with directory structure based on current date
        object_key = f'ingredients/{current_date}/ingredients_{current_time}.json'

        # Create directories in MinIO if they don't exist
        directory_path = os.path.dirname(object_key)
        s3.put_object(Bucket=bucket_name, Key=f'{directory_path}/')

        # Upload JSON data as an object to MinIO
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=json_data)
    
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
        
