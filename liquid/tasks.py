from typing import Mapping, Iterable, Union

import cv2
import json
import time
import webvtt
import string
import datetime as dt

from . import s3, celery
from .models import Liquid
from .db import db_session
from .rekognition import get_sqs_message, VideoDetector
from .util import numpy_to_binary


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """This function sets up Celery Beat"""
    sender.add_periodic_task(60.0, check_sqs.s(), name="check SQS queue every minute")


@celery.task(name="app.tasks.check_sqs")
def check_sqs() -> str:
    """
    Running on `Beat` thread

    This task is called periodically by celery beat to check
    for when a video processing job is complete

    Check rekognition results:
    One scenario is checking for new messages in an AWS SQS queue.
    The queue is subscribed to a SNS channel that gets notified
    when a rekognition task is completed. If message is found in
    queue, then get rekognition results based on the rekognition
    job id.

    Check transcriber results:
    Another scenario is checking for new job completetion in the
    transcriber service.
    """

    def get_results(job_id):
        liquid = Liquid.query.filter(Liquid.job_id == job_id).first()
        detector = VideoDetector(job_id, liquid.treatment_id)
        if not detector.get_results():
            process_job_data.apply_async(args=[detector.labels, job_id])

    # check sqs for rekognition results
    get_sqs_message(get_results)

    return "done"


@celery.task(name="app.tasks.celery_test")
def celery_test(message: str) -> str:
    """DEV ONLY"""
    # randomly update something in the db show that connections works
    liquid = Liquid.query.filter(Liquid.id == 3).first()
    liquid.active = True
    db_session.add(liquid)
    db_session.commit()
    return "done"


@celery.task(name="app.tasks.process_job_data")
def process_job_data(data: Union[Mapping, Iterable], job_id: str) -> bool:
    """Preprocess data based on treatment id

    Args:
        data: data from model output
        job_id: job id to look up corresponding liquid
    Returns:
        Success or not
    """
    liquid = Liquid.query.filter(Liquid.job_id == job_id).first()
    success = True
    if liquid.treatment_id == 1:
        success = _process_speech_search(data, liquid)
    elif liquid.treatment_id == 2:
        success = _process_image_search(data, liquid)
    elif liquid.treatment_id == 3:
        success = _process_text_search(data, liquid)
    else:
        print("Error - treatment id not found")
    return success


def _process_speech_search(data: Union[Mapping, Iterable], liquid: Liquid) -> None:
    """Process transcription output by converting to json format

    1. get transcription vtt s3 bucket location
    2. convert vtt to json formation
    3. upload json file to <liquid_path>, which we get using s3.get_s3_liquid_path

    # TODO (look at `_process_text_search` as example)
    """

    def time_into_milliseconds(self, time_string):
        """Utility function to turn time string into milliseconds."""
        hours = int(time_string[:2])
        mins = int(time_string[3:5])
        seconds = float(time_string[6:])
        return int(hours * 3600000 + mins * 60000 + seconds * 1000)

    def make_caption_dict(self, vtt):
        """Makes a JSON dictionary from AWS transcribed vtt into a JSON dictionary"""

        if vtt[-4:] == ".vtt":
            captions = webvtt.read(vtt)
        else:
            if vtt[-4:] == ".srt":
                captions = webvtt.from_srt(vtt)
            elif vtt[-4:] == ".sbv":
                captions = webvtt.from_sbv(vtt)
            else:
                return "File format not accepted"

        word_locations = dict()

        for line in captions:
            total_time = dt.strptime(line.start, "%H:%M:%S.%f")
            text = (
                line.text.translate(str.maketrans("", "", string.punctuation))
                .lower()
                .split()
            )
            time_interval = dt.strptime(line.end, "%H:%M:%S.%f") - dt.strptime(
                line.start, "%H:%M:%S.%f"
            )
            for i in range(len(text)):
                curr_time = (total_time + time_interval * i / len(text)).strftime(
                    "%H:%M:%S.%f"
                )
                word_locations.setdefault(text[i], [])
                word_locations[text[i]].append(self.time_into_milliseconds(curr_time))

        return word_locations

    vtt = data
    capt_dict = make_caption_dict(vtt)
    path = s3.get_s3_liquid_path(liquid.user_id, liquid.video.id, liquid.id)
    key = f"{path}/captions.json"
    success = s3.put_object(
        obj=json.dumps(capt_dict),
        key=key,
        content_type="application/json",
    )
    if not success:
        print("Error uploading json file.")
        return False

    # update db entry
    liquid.processing = False
    liquid.url = s3.get_object_url(key)
    db_session.add(liquid)
    db_session.commit()

    return True


def _process_image_search(data: Union[Mapping, Iterable], liquid: Liquid) -> bool:
    """Process label detector results from rekognition

    #TODO convert print lines to log statements

    1. load video from url in opencv VideoCapture
    2. for each label found in data, get frame based on timestamp
    3. save each frame to s3
    4. add url for saved frame back to the data
    5. add data to s3
    6. update db with new liquid attributes

    Args:
        data: results from rekognition job
        liquid: liquid object
    Returns:
        success
    """
    path = s3.get_s3_liquid_path(liquid.user_id, liquid.video.id, liquid.id)
    frames_path = f"{path}/frames"

    # for logging purposes
    get_frame_time = 0
    upload_frame_time = 0

    # use opencv (cv2) to get frames based on timestamp
    video_capture = cv2.VideoCapture(liquid.video.url)

    prev_timestamp = 0
    for label in data:
        timestamp = label["Timestamp"]
        frame_key = f"{frames_path}/{timestamp}.jpg"

        if timestamp != prev_timestamp:
            # get frame based on timestamp
            start = time.time()
            video_capture.set(cv2.CAP_PROP_POS_MSEC, timestamp)
            _, frame = video_capture.read()
            end = time.time()
            get_frame_time += end - start

            # save frame to s3 bucket
            start = time.time()
            success = s3.upload_fileobj(
                obj=numpy_to_binary(frame), key=frame_key, content_type="image/jpeg"
            )
            if not success:
                print(f"Error uploading {timestamp}")
                return False
            end = time.time()
            upload_frame_time += end - start

        # add url to data object
        label["FrameURL"] = s3.get_object_url(frame_key)

        prev_timestamp = timestamp

    key = f"{path}/data.json"
    success = s3.put_object(
        obj=json.dumps(data),
        key=key,
        content_type="application/json",
    )
    if not success:
        print("Error uploading json file.")
        return False

    print(f"Total of {get_frame_time} seconds to get frames from opencv")
    print(f"Total of {upload_frame_time} seconds to upload frame")

    # update db entry
    liquid.processing = False
    liquid.url = s3.get_object_url(key)
    db_session.add(liquid)
    db_session.commit()

    return True


def _process_text_search(data: Union[Mapping, Iterable], liquid: Liquid) -> bool:
    """Process text detector results from rekognition

    #TODO convert print lines to log statements

    1. add data to s3
    2. update db with new liquid attributes

    Args:
        data: results from rekognition job
        liquid: liquid object
    Returns:
        success
    """
    path = s3.get_s3_liquid_path(liquid.user_id, liquid.video.id, liquid.id)
    key = f"{path}/data.json"
    success = s3.put_object(
        obj=json.dumps(data),
        key=key,
        content_type="application/json",
    )
    if not success:
        print("Error uploading json file.")
        return False

    # update db entry
    liquid.processing = False
    liquid.url = s3.get_object_url(key)
    db_session.add(liquid)
    db_session.commit()

    return True
