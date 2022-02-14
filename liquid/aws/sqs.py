from typing import Callable, Dict
import json
import boto3
from flask import current_app as app


aws_sqs_queue_url = app.config["AWS_SQS_QUEUE_URL"]
aws_sqs = boto3.client("sqs", region_name="us-east-1")


def put_message(msg_body: Dict):
    """ Put message in sqs queue.

    Args:
        msg_body: dictionary, must contain keys: "Type" and "JobId"
    """
    aws_sqs.send_message(
        QueueUrl=aws_sqs_queue_url,
        DelaySeconds=10,
        MessageBody=json.dumps(msg_body),
    )


def get_message(cb: Callable):
    """Poll for msgs from AWS SQS queue. Messages will appear in the queue when
    video processing tasks are completed.

    Args:
        cb: the function to call once message is retreived from the queue
    """
    sqs_response = aws_sqs.receive_message(
        QueueUrl=aws_sqs_queue_url, MessageAttributeNames=["ALL"], MaxNumberOfMessages=1
    )
    if "Messages" in sqs_response:
        for message in sqs_response["Messages"]:
            msg_body = json.loads(message["Body"])

            # determine message type
            job_id = None
            if msg_body["Type"] == "Notification":
                rek_msg = json.loads(msg_body["Message"])  # message from rekognition
                job_id = rek_msg["JobId"]
            elif msg_body["Type"] == "Default":
                job_id = msg_body["JobId"]
            else:
                print("Invalid Message.")
                return False

            # delete msg from queue
            if cb(job_id):
                aws_sqs.delete_message(
                    QueueUrl=aws_sqs_queue_url, ReceiptHandle=message["ReceiptHandle"]
                )



