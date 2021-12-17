""" AWS helper functions """
from flask import current_app as app
from botocore.exceptions import ClientError
import logging
import boto3


s3_client = boto3.client(
    "s3",
    aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
)


def upload_file(file_obj, bucket, path, content_type, ext, object_name=None):
    """Upload a file to an S3 bucket

    Args:
        file_name: File to upload
        bucket: Bucket to upload to
        user_id: User ID
        content_type: type of content
        ext: extension (mp4, png, or jpeg)
        object_name: S3 object name

    Return:
        True if file was uploaded, else False
    """
    try:
        s3_client.upload_fileobj(
            file_obj,
            bucket,
            f"{path}/{object_name}.{ext}",
            ExtraArgs={"ContentType": content_type, "ACL": "public-read"},
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True
