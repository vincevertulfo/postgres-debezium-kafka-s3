from confluent_kafka.schema_registry import Schema, SchemaRegistryClient

schema_registry_url = "http://localhost:8085" 
schema_registry_client = SchemaRegistryClient({"url":schema_registry_url })

schema_version = schema_registry_client.get_latest_version(
    'postgres.public.ingredients-value'
)
schema_id = schema_version.schema_id

schema = schema_registry_client.get_schema(schema_id)

schema_str = schema.schema_str