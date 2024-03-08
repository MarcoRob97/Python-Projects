import boto3
from datetime import datetime
import pandas as pd
from sshtunnel import SSHTunnelForwarder
import pymysql

# Connection to v2 production
ssh_hostname = '3.137.79.108'
SSH_username = 'magnum'
ssh_key_file = "//saturnv2/FileDump/Data/magnum_v2_ed25519.pem"

mysql_hostname = 'v2-onerater-database.cluster-c5xtvyrmqz7e.us-east-2.rds.amazonaws.com'
mysql_server_port = 3306
username_db = 'magnum'
password_db = 'Pasword'

with SSHTunnelForwarder((ssh_hostname), ssh_username=SSH_username, ssh_pkey=ssh_key_file, remote_bind_address=(mysql_hostname, mysql_server_port)
) as tunnel:
    print("****SSH Tunnel Established****")

    db = pymysql.connect(
        host='127.0.0.1', user=username_db,
        password=password_db, port=tunnel.local_bind_port
    )
    data_set = pd.read_sql_query('''
       select * from v2_onerater_com.vw_contracts where idate = curdate();
        '''
        , db)               
                
    db.close()

# Replace these with your values from temporary credentials process
AWS_ACCESS_KEY_ID = "AKIAUJ2BU4GPVKD3FEXR"
AWS_SECRET_ACCESS_KEY = "secretaccesskey"

# Replace these placeholders with your actual values
REGION_NAME = "us-east-2"  # Replace with your desired AWS region
BUCKET_NAME = "magnum-bucket-marc"  # Replace with the name of your S3 bucket

# Create a session with temporary credentials using boto3 Session object
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

# Get the S3 client using the temporary credentials
s3_client = session.client("s3")

def upload_to_s3(file_path, object_key):
  try:
    s3_client.upload_file(file_path, BUCKET_NAME, object_key)
    print(f"File '{file_path}' uploaded to S3 bucket '{BUCKET_NAME}' as '{object_key}'")
  except Exception as e:
    print(f"Error uploading file: {e}")


# Write DataFrame to a CSV file
current_date = datetime.now().strftime("%m_%d_%Y") # Get the current date
file_to_upload = 'E:\\today_records.csv'
data_set.to_csv(file_to_upload, index=False)

# Example usage:
object_key = f"today_records_{current_date}.csv" 

upload_to_s3(file_to_upload, object_key)