import boto3
import json
from flask import current_app as app


aws_sqs_queue_url = app.config["AWS_SQS_QUEUE_URL"]
aws_rek = boto3.client("rekognition", region_name="us-east-1")
aws_sns = boto3.client("sns", region_name="us-east-1")
aws_sqs = boto3.client("sqs", region_name="us-east-1")


def get_sqs_message(cb):
    """ poll for msg """
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


class VideoSubmitter:
    bucket = ""
    video = ""
    job_id = ""
    role_arn = ""
    sns_topic_arn = ""
    sqs_queue_arn = ""
    treatment_id = ""

    def __init__(
        self, role_arn, sns_topic_arn, sqs_queue_arn, bucket, video, treatment_id
    ):
        self.role_arn = role_arn
        self.sns_topic_arn = sns_topic_arn
        self.sqs_queue_arn = sqs_queue_arn
        self.bucket = bucket
        self.video = video
        self.treatment_id = treatment_id

        # subscribe the sqs to the sns topic (if not already)
        aws_sns.subscribe(
            TopicArn=self.sns_topic_arn, Protocol="sqs", Endpoint=self.sqs_queue_arn
        )

    def do_detection(self):
        """ TODO """
        if self.treatment_id == 1:
            pass
        elif self.treatment_id == 2:
            self._do_image_detection()
        elif self.treatment_id == 3:
            self._do_text_detection()
        else:
            print("invalid treatment id")

    def _do_image_detection(self):
        """TODO
        Labels generic images...
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
        """ Searches for text in the video. """
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

    def __init__(self, job_id, treatment_id):
        self.job_id = job_id
        self.treatment_id = treatment_id

    def get_results(self):
        """TODO"""
        if self.treatment_id == 1:
            pass
        elif self.treatment_id == 2:
            return self._get_image_detection_results()
        elif self.treatment_id == 3:
            return self._get_text_detection_results()
        else:
            print("Invalid treatment")
            return None

    def _get_image_detection_results(self):
        """TODO"""
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
        """TODO"""
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
