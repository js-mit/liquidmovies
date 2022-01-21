""" S3 helper functions """
from typing import Union, Mapping, Iterable
from io import IOBase
from flask import current_app as app
from botocore.exceptions import ClientError
from urllib.parse import urlparse
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


def get_s3_video_path(user_id: int, video_id: int) -> str:
    """Gets s3 video path
    path structure: users/<user_id>/videos/<video_id>

    Args:
        user_id: user_id
        video_id: video_id
    Returns:
        string url
    """
    return f"users/{user_id}/videos/{video_id}"


def get_s3_liquid_path(user_id: int, video_id: int, liquid_id: int) -> str:
    """Gets s3 liquid path
    path structure: users/<user_id>/videos/<video_id>/liquids/<liquid_id>

    Args:
        user_id: user_id
        video_id: video_id
        treatment_id: liquid_id
    Returns:
        string url
    """
    return f"users/{user_id}/videos/{video_id}/liquids/{liquid_id}"


def get_object_url(key: str) -> str:
    """Get s3 object url
    url structure: <s3_bucket>.s3.amazonaws.com/<key>

    Args:
        path: the object path
        filename: object filename
    Return:
        url in string
    """
    return f"https://{s3_bucket}.s3.amazonaws.com/{key}"


def put_object(obj: IOBase, key: str, content_type: str) -> bool:
    """Upload object using s3 boto put_object function

    Args:
        fname: filename
        key: path + filename and extention to save in s3
        content_type: "application/json" if json, etc
    Return
        success
    """
    try:
        s3_client.put_object(
            ACL="public-read",
            Bucket=s3_bucket,
            Body=obj,
            ContentType=content_type,
            Key=key,
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_fileobj(obj: IOBase, key: str, content_type: str) -> bool:
    """Upload object using s3 boto3 upload_fileobj function
    Use this is file is big and may require multithreading or a stream

    Args:
        fname: filename
        key: path + filename and extention to save in s3
        content_type: "video/mp4" if video, etc
    Return
        success
    """
    try:
        s3_client.upload_fileobj(
            obj,
            s3_bucket,
            key,
            ExtraArgs={"ContentType": content_type, "ACL": "public-read"},
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True


def _download_liquid(key: str) -> Union[Mapping, Iterable]:
    """Get liquid data stored in s3 bucket

    Args:
        key: key of s3 object (use `get_s3_liquid_path` func)
    Returns:
        liquid data as python object
    """
    data = None
    milliseconds = str(int(round(time.time() * 1000)))
    tmp_file = f"data-{milliseconds}.json"
    s3_client.download_file(s3_bucket, key, tmp_file)
    with open(tmp_file) as f:
        data = json.load(f)
        f.close()
    os.remove(tmp_file)
    return data


def download_liquid_by_key(key: str) -> Union[Mapping, Iterable]:
    return _download_liquid(key)


def download_liquid_by_url(url: str) -> Union[Mapping, Iterable]:
    key = urlparse(url).path[1:]
    return _download_liquid(key)
