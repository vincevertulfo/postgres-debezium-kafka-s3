import boto3

def initialise_s3_client(access_key, secret_key, endpoint, region='us-east-1'):
    """
    Initializes and returns an S3 client with the provided credentials and endpoint.
    
    Parameters:
    - access_key (str): AWS access key ID.
    - secret_key (str): AWS secret access key.
    - endpoint (str): Endpoint URL of the S3 service (e.g., MinIO).
    - region (str, optional): AWS region. Default is 'us-east-1'.
    
    Returns:
    - boto3.client: Initialized S3 client.
    """
    s3_client = boto3.client('s3',
                             endpoint_url=endpoint,
                             aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key,
                             region_name=region
                            )
    return s3_client

def list_s3_buckets(s3_client):
    """
    Lists all S3 buckets using the provided S3 client and prints their names.
    
    Parameters:
    - s3_client (boto3.client): Initialized S3 client.
    """
    response = s3_client.list_buckets()
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')

# Credentials and Connection Info
access_key = "minio"
secret_key = "minio123"
endpoint = "http://localhost:9000"
region = "us-east-1"  # Dummy

# Initialize an S3 client
s3 = initialise_s3_client(access_key, secret_key, endpoint, region)

# List all S3 buckets
list_s3_buckets(s3)
