import cv2
import json
import io
import time

from . import s3, celery
from .models import Liquid
from .db import db_session


@celery.task(name="app.tasks.celery_test")
def celery_test(message):
    # randomly update something in the db show that connections works
    liquid = Liquid.query.filter(Liquid.id == 3).first()
    liquid.active = True
    db_session.add(liquid)
    db_session.commit()
    print(liquid.treatment_id)
    return "done"


@celery.task(name="app.tasks.process_job_data")
def process_job_data(data, job_id):
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
    else:
        print("Error - treatment id not found")
    return success


def _process_speech_search(data, liquid):
    return None


def _process_image_search(data, liquid):
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
    s3.put_object(
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


def numpy_to_binary(arr):
    """ Convert video from numpy array to a binary object in memory """
    _, buffer = cv2.imencode(".jpg", arr)
    io_buf = io.BytesIO(buffer)
    return io_buf