# import boto3
# import json
# from config import Config

# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
# )

# def upload_execution_result(execution_id, data):
#     s3_client.put_object(
#         Bucket=Config.AWS_S3_BUCKET,
#         Key=f'executions/{execution_id}.json',
#         Body=json.dumps(data),
#         ContentType='application/json'
#     )

# def get_execution_result(execution_id):
#     try:
#         response = s3_client.get_object(
#             Bucket=Config.AWS_S3_BUCKET,
#             Key=f'executions/{execution_id}.json'
#         )
#         return json.loads(response['Body'].read().decode())
#     except s3_client.exceptions.NoSuchKey:
#         return None
#     except Exception as e:
#         return None


# backend/utils/storage.py

import boto3
from config import Config
import json
import logging

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.AWS_REGION  # Ensure region is specified
)

def upload_execution_result(execution_id, data):
    """
    Uploads the execution result to the specified S3 bucket.
    
    Parameters:
        execution_id (int): The ID of the execution.
        data (dict): The execution data to upload.
    
    Returns:
        bool: True if upload is successful, False otherwise.
    """
    try:
        logging.debug(f"Attempting to upload execution {execution_id} to S3.")
        s3_client.put_object(
            Bucket=Config.AWS_S3_BUCKET,
            Key=f'executions/{execution_id}.json',  # Use integer ID
            Body=json.dumps(data),
            ContentType='application/json'
        )
        logging.info(f"Successfully uploaded execution {execution_id} to S3.")
        return True
    except Exception as e:
        logging.error(f"Failed to upload execution {execution_id} to S3: {e}")
        return False

def get_execution_result(execution_id):
    """
    Retrieves the execution result from the specified S3 bucket.
    
    Parameters:
        execution_id (int): The ID of the execution.
    
    Returns:
        dict or None: The execution data if found, else None.
    """
    try:
        response = s3_client.get_object(
            Bucket=Config.AWS_S3_BUCKET,
            Key=f'executions/{execution_id}.json'
        )
        content = response['Body'].read().decode('utf-8')
        logging.info(f"Successfully retrieved execution {execution_id} from S3.")
        return json.loads(content)
    except s3_client.exceptions.NoSuchKey:
        logging.warning(f"Execution {execution_id} not found in S3.")
        return None
    except Exception as e:
        logging.error(f"Failed to retrieve execution {execution_id} from S3: {e}")
        return None
