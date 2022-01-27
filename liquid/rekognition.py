from typing import Callable
import boto3
from flask import current_app as app

import webvtt, string, json
from datetime import datetime as dt
from datetime import timezone

from . import s3

aws_sqs_queue_url = app.config["AWS_SQS_QUEUE_URL"]
aws_rek = boto3.client("rekognition", region_name="us-east-1")
aws_trs = boto3.client("transcribe", region_name="us-east-1")
aws_sns = boto3.client("sns", region_name="us-east-1")
aws_sqs = boto3.client("sqs", region_name="us-east-1")


def get_sqs_message(cb: Callable):
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
            # get rek_msg to get job_id
            notification = json.loads(message["Body"])
            rek_msg = json.loads(notification["Message"])

            # get results from rek using this cb
            cb(rek_msg["JobId"])

            # delete msg from queue
            aws_sqs.delete_message(
                QueueUrl=aws_sqs_queue_url, ReceiptHandle=message["ReceiptHandle"]
            )
            print("here--------", message)


class VideoSubmitter:
    bucket = ""
    video = ""
    job_id = ""
    role_arn = ""
    sns_topic_arn = ""
    sqs_queue_arn = ""
    treatment_id = ""
    liquid = None

    def __init__(
        self,
        role_arn: str,
        sns_topic_arn: str,
        sqs_queue_arn: str,
        bucket: str,
        video: str,
        treatment_id: int,
        liquid: str,
    ):
        """
        Args:
            role_arn: arn for the rek service role
            sns_topic_arn: arn for the sns topic
            sqs_queue_arn: arn for the sqs queue
            bucket: the name of the s3 bucket where the video is located
            video: the path to the video in the s3 bucket
            treatment_id: the treatment id to determine which model to run
            liquid: the liquid object to perform liquid operations
        """
        self.role_arn = role_arn
        self.sns_topic_arn = sns_topic_arn
        self.sqs_queue_arn = sqs_queue_arn
        self.bucket = bucket
        self.video = video
        self.treatment_id = treatment_id
        self.liquid = liquid

        # subscribe the sqs to the sns topic (if not already)
        aws_sns.subscribe(
            TopicArn=self.sns_topic_arn, Protocol="sqs", Endpoint=self.sqs_queue_arn
        )

    def do_detection(self):
        """Generic function that determines with kind of detection to call based
        on treatment type.
        """
        if self.treatment_id == 1:
            self._do_text_transcription()
        elif self.treatment_id == 2:
            self._do_image_detection()
        elif self.treatment_id == 3:
            self._do_text_detection()
        else:
            print("invalid treatment id")

    def _do_text_transcription(self):
        """Calls AWS Rekognition to create captions for the video."""
        video_uri = s3.get_object_url(self.video)
        job_id = f"transcription-service-{self.liquid.id}"
        response = aws_trs.start_transcription_job(
            TranscriptionJobName=job_id,
            Media={"MediaFileUri": video_uri},
            MediaFormat="mp4",
            LanguageCode="en-US",
            Subtitles={"Formats": ["vtt"]},
            OutputBucketName=self.bucket,
            OutputKey=s3.get_s3_liquid_path(
                self.liquid.user_id, self.liquid.video_id, self.liquid.id
            ),
        )
        self.job_id = job_id

        # Adding a message to queue for get_sqs_message function to pickup
        # Send message to SQS queue
        response = aws_sqs.send_message(
            QueueUrl=aws_sqs_queue_url,
            DelaySeconds=10,
            MessageAttributes={
                "Title": {"DataType": "String", "StringValue": "Hi"},
            },
            # TODO:EDIT THIS
            MessageBody=(f'"Message": { "JobId": {job_id} }'),
        )

    def _do_image_detection(self):
        """Calls AWS Rekognition label detection model to score each frame of
        the video.
        """
        response = aws_rek.start_label_detection(
            Video={"S3Object": {"Bucket": self.bucket, "Name": self.video}},
            NotificationChannel={
                "RoleArn": self.role_arn,
                "SNSTopicArn": self.sns_topic_arn,
            },
            JobTag="liquid-label-detection",
        )

        self.job_id = response["JobId"]

    def _do_text_detection(self):
        """Calls AWS Rekognition text detection model to detect text in each frame
        of the video
        """
        response = aws_rek.start_text_detection(
            Video={"S3Object": {"Bucket": self.bucket, "Name": self.video}},
            NotificationChannel={
                "RoleArn": self.role_arn,
                "SNSTopicArn": self.sns_topic_arn,
            },
            JobTag="liquid-text-detection",
        )

        self.job_id = response["JobId"]


class VideoDetector:
    job_id = ""
    treatment_id = None
    labels = []
    duration = 0

    def __init__(self, job_id: str, treatment_id: int):
        """
        Args:
            job_id: the id of the job to get results from
            treatment_id: the treatment that was used for the liquid
        """
        self.job_id = job_id
        self.treatment_id = treatment_id

    def get_results(self):
        """Generic function to get results of model based on treatment id."""
        if self.treatment_id == 1:
            return self._get_transcription_results()
        elif self.treatment_id == 2:
            return self._get_image_detection_results()
        elif self.treatment_id == 3:
            return self._get_text_detection_results()
        else:
            print("Invalid treatment")
            return None

    def _get_transcription_results(self):
        """Get text transcription results from aws."""

        response = aws_trs.get_transcription_job(TranscriptionJobName=liquid.job_id)
        if response["TranscriptionJob"]["TranscriptionJobStatus"] not in [
            "COMPLETED",
            "FAILED",
        ]:
            return True
        self.labels = response["TranscriptionJob"]["Subtitles"]["SubtitleFileUris"][0]
        return False

    def _get_image_detection_results(self):
        """Get image detection result from aws."""
        pagination_token = ""
        finished = False

        while finished == False:

            response = aws_rek.get_label_detection(
                JobId=self.job_id,
                MaxResults=500,
                NextToken=pagination_token,
                SortBy="TIMESTAMP",
            )

            self.labels.extend(response["Labels"])

            if "NextToken" in response:
                pagination_token = response["NextToken"]
            else:
                finished = True

    def _get_text_detection_results(self):
        """Get text detection result from aws."""
        pagination_token = ""
        finished = False

        while finished == False:

            response = aws_rek.get_text_detection(
                JobId=self.job_id,
                MaxResults=500,
                NextToken=pagination_token,
            )

            self.labels.extend(response["TextDetections"])

            if "NextToken" in response:
                pagination_token = response["NextToken"]
            else:
                finished = True
