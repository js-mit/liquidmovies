""" S3 helper functions """
from flask import current_app as app
from botocore.exceptions import ClientError
import logging
import boto3
import json
import os
import time


s3_client = boto3.client(
    "s3",
    aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
)
s3_bucket = app.config["AWS_S3_BUCKET"]


def get_s3_video_path(user_id, video_id):
    """ Gets s3 video path
    path structure: users/<user_id>/videos/<video_id>

    Args:
        user_id: user_id
        video_id: video_id
    Returns:
        string url
    """
    return f"users/{user_id}/videos/{video_id}"


def get_s3_liquid_path(user_id, video_id, liquid_id):
    """ Gets s3 liquid path
    path structure: users/<user_id>/videos/<video_id>/liquids/<liquid_id>

    Args:
        user_id: user_id
        video_id: video_id
        treatment_id: liquid_id
    Returns:
        string url
    """
    return f"users/{user_id}/videos/{video_id}/liquids/{liquid_id}"


def get_object_url(key):
    """Get s3 object url
    url structure: <bucket>.s3.amazonaws.com/<key>

    Args:
        path: the object path
        filanem: object filename
    Return:
        url in string
    """
    return f"https://{s3_bucket}.s3.amazonaws.com/{key}"


def upload(file_obj, key, content_type):
    """Upload a file to an S3 bucket

    Decides whether to use boto3's `upload_file` or
    `upload_fileobj` depending on content type

    Args:
        file_name: File to upload
        key: path + filename and extention
        content_type: type of content

    Return:
        True if file was uploaded, else False
    """
    try:
        if "json" in content_type:
            milliseconds = str(int(round(time.time() * 1000)))
            tmp_file = f"data-{milliseconds}.json"
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(file_obj, f, ensure_ascii=False, indent=4)
                s3_client.upload_file(
                    tmp_file,
                    s3_bucket,
                    key,
                    ExtraArgs={"ContentType": content_type, "ACL": "public-read"},
                )
                os.remove(tmp_file)
        else:
            s3_client.upload_fileobj(
                file_obj,
                s3_bucket,
                key,
                ExtraArgs={"ContentType": content_type, "ACL": "public-read"},
            )
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_liquid_data(user_id, video_id, liquid_id):
    """ TODO """
    key = get_s3_liquid_path(user_id, video_id, liquid_id)
    with open("tmp.json", 'wb') as f:
        s3_client.download_fileobj(s3_bucket, key, f)
        return f
