import boto3
from datetime import datetime

# Define the source and destination bucket names
SOURCE_BUCKET_NAME = 'source-bucket'
DESTINATION_BUCKET_NAME = 'destination-bucket'

def lambda_handler(event, context):
    # Create S3 client
    s3_client = boto3.client('s3')
    
    try:
        # Get the current date in the format MM_DD_YYYY
        current_date = datetime.now().strftime("%m_%d_%Y")
        
        # Construct the object key based on the current date
        object_key = f"today_records_{current_date}.csv"
        
        # Copy object from source bucket to destination bucket
        copy_source = {'Bucket': SOURCE_BUCKET_NAME, 'Key': object_key}
        s3_client.copy_object(CopySource=copy_source, Bucket=DESTINATION_BUCKET_NAME, Key=object_key)
        
        print(f"Object '{object_key}' copied from '{SOURCE_BUCKET_NAME}' to '{DESTINATION_BUCKET_NAME}' successfully!")
        
        
    except Exception as e:
        print("Error:", e)