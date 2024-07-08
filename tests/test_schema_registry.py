from confluent_kafka.schema_registry import SchemaRegistryClient

# Schema Registry URL
schema_registry_url = "http://localhost:8085"

# Initialize Schema Registry client
schema_registry_client = SchemaRegistryClient({"url": schema_registry_url})

# Get all registered subjects
subjects = schema_registry_client.get_subjects()

print("Registered Subjects:")
for subject in subjects:
    print(subject)

# Get the latest schema version and retrieve schema string for each subject
for subject in subjects:
    latest_version = schema_registry_client.get_latest_version(subject).schema_id
    schema_str = schema_registry_client.get_schema(latest_version).schema_str
    
    print(f"\nSchema String for '{subject}':")
    print(schema_str)