"""MiniO client configuration."""

import json
import boto3
from botocore.client import Config
from content_service.core.config import settings
import logging

logger = logging.getLogger(__name__)


s3_client = boto3.client(
    "s3",
    endpoint_url=settings.MINIO_ENDPOINT,
    aws_access_key_id=settings.MINIO_ACCESS_KEY,
    aws_secret_access_key=settings.MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)


def init_minio():
    """Create bucket if it doesn't exist and set it to public."""
    try:
        s3_client.head_bucket(Bucket=settings.MINIO_BUCKET)
    except Exception:
        s3_client.create_bucket(Bucket=settings.MINIO_BUCKET)
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{settings.MINIO_BUCKET}/*"],
                }
            ],
        }
        s3_client.put_bucket_policy(
            Bucket=settings.MINIO_BUCKET, Policy=json.dumps(policy)
        )
    logger.info("MinIO bucket '%s' is ready.", settings.MINIO_BUCKET)
