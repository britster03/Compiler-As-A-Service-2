# backend/utils/storage.py
import boto3
from config import Config
import json
import logging

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
)

def upload_execution_result(execution_id, data):
    try:
        s3_client.put_object(
            Bucket=Config.AWS_S3_BUCKET,
            Key=f'executions/{execution_id}.json',
            Body=json.dumps(data),
            ContentType='application/json'
        )
    except Exception as e:
        logging.error(f"Failed to upload execution result to S3: {e}")

def get_execution_result(execution_id):
    try:
        response = s3_client.get_object(
            Bucket=Config.AWS_S3_BUCKET,
            Key=f'executions/{execution_id}.json'
        )
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)
    except s3_client.exceptions.NoSuchKey:
        return None
    except Exception as e:
        logging.error(f"Failed to retrieve execution result from S3: {e}")
        return None
