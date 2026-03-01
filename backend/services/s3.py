import boto3
from config.config import config

s3_client = boto3.client(
    "s3",
    region_name=config.S3_REGION,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
)

def generate_presigned_url(bucket: str, key: str) -> str:
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=config.PRESIGNED_URL_EXPIRY
    )