import boto3


aws_rek = boto3.client("rekognition", region_name="us-east-1")
aws_sns = boto3.client("sns", region_name="us-east-1")


class VideoSubmitter:
    bucket = ""
    video = ""
    job_id = ""
    role_arn = ""
    sns_topic_arn = ""
    lambda_arn = ""
    treatment_id = ""

    def __init__(
        self, role_arn, sns_topic_arn, lambda_arn, bucket, video, treatment_id
    ):
        self.role_arn = role_arn
        self.sns_topic_arn = sns_topic_arn
        self.lambda_arn = lambda_arn
        self.bucket = bucket
        self.video = video
        self.treatment_id = treatment_id

        # subscribe the lambda func to the sns topic
        aws_sns.subscribe(
            TopicArn=self.sns_topic_arn, Protocol="lambda", Endpoint=self.lambda_arn
        )

    def do_label_detection(self):
        response = aws_rek.start_label_detection(
            Video={"S3Object": {"Bucket": self.bucket, "Name": self.video}},
            NotificationChannel={
                "RoleArn": self.role_arn,
                "SNSTopicArn": self.sns_topic_arn,
            },
            JobTag="liquid",
        )

        self.job_id = response["JobId"]


class VideoDetector:
    job_id = ""
    labels = []
    duration = 0

    def __init__(self, job_id):
        self.job_id = job_id

    def get_results(self):
        pagination_token = ""
        finished = False

        while finished == False:

            response = aws_rek.get_label_detection(
                JobId=self.job_id,
                MaxResults=500,
                NextToken=pagination_token,
                SortBy="TIMESTAMP",
            )

            assert(isinstance(response["Labels"], list))

            self.labels.extend(response["Labels"])
            self.duration = str(response["VideoMetadata"]["DurationMillis"])

            if "NextToken" in response:
                pagination_token = response["NextToken"]
            else:
                finished = True
