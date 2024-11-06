

# backend/utils/storage.py
import boto3

import json
import logging
from dotenv import load_dotenv
load_dotenv()
import os
# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def upload_execution_result(execution_id, data):
    try:
        s3_client.put_object(
            Bucket=os.getenv('AWS_S3_BUCKET'),
            Key=f'executions/{execution_id}.json',
            Body=json.dumps(data),
            ContentType='application/json'
        )
        logging.info(f"Successfully uploaded execution {execution_id} to S3.")
        return True
    except Exception as e:
        logging.error(f"Failed to upload execution result to S3: {e}")
        return False


def get_execution_result(execution_id):
    try:
        response = s3_client.get_object(
            Bucket=os.getenv('AWS_S3_BUCKET'),
            Key=f'executions/{execution_id}.json'
        )
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)
    except s3_client.exceptions.NoSuchKey:
        return None
    except Exception as e:
        logging.error(f"Failed to retrieve execution result from S3: {e}")
        return None


def test_upload_execution_result(client):
    execution_id = 1
    data = {"output": "Hello, S3!", "error": ""}
    success = upload_execution_result(execution_id, data)
    assert success is True

    # Retrieve the uploaded file
    retrieved_data = get_execution_result(execution_id)
    assert retrieved_data == data

def test_upload_invalid_bucket(client, monkeypatch):
    monkeypatch.setattr('utils.storage.Config.AWS_S3_BUCKET', 'invalid-bucket-name')
    execution_id = 2
    data = {"output": "Test", "error": ""}
    success = upload_execution_result(execution_id, data)
    assert success is False
