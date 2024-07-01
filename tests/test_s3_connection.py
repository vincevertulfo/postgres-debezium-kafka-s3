import boto3

# Credentials and Connection Info
access_key = "minio"
secret_key = "minio123"
endpoint = "http://localhost:9000"
region = "us-east-1" # Dummy

# Initialize an S3 client
s3 = boto3.client('s3',
                  endpoint_url=endpoint,
                  aws_access_key_id=access_key,
                  aws_secret_access_key=secret_key,
                  region_name='us-east-1',
                 )

#List all S3 buckets
response = s3.list_buckets()

# Print bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')
