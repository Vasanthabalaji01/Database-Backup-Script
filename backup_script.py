import os
import subprocess
import datetime
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Database Connection Details
    db_host = "your_database_host"
    db_name = "your_database_name"
    db_user = "your_database_user"
    db_password = "your_database_password"

    # S3 Bucket Details
    s3_bucket_name = "your_s3_bucket_name"
    s3_object_key = f"backups/{db_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.sql"

    # Backup Command
    backup_command = f"pg_dump -h {db_host} -U {db_user} -d {db_name} -Fc -f /tmp/{db_name}.dump"

    # Run Backup Command
    try:
        subprocess.run(backup_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing backup command: {e}")
        return {"statusCode": 500, "body": "Backup failed"}

    # Upload Backup to S3
    s3_client = boto3.client("s3")

    try:
        s3_client.upload_file(f"/tmp/{db_name}.dump", s3_bucket_name, s3_object_key)
    except ClientError as e:
        print(f"Error uploading backup to S3: {e}")
        return {"statusCode": 500, "body": "Backup upload to S3 failed"}

    # Clean up temporary backup file
    os.remove(f"/tmp/{db_name}.dump")

    return {"statusCode": 200, "body": "Backup successful"}
