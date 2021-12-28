import cv2
import json
import io
import time

from . import s3


def render_data(data, treatment_id):
    """ Render data for the frontend based on treatment id

    Args:
        data: data from s3 bucket
        treatment_id: type of treatment
    Returns
        Processed data as python object
    """
    results = None
    if treatment_id == 1:
        results = _render_speech_search(data)
    elif treatment_id == 2:
        results = _render_image_search(data)
    else:
        print("Error - treatment id not found")

    return results


def _render_speech_search(data):
    # TODO
    return data


def _render_image_search(data):
    # TODO
    return data


# def process_data(data, liquid, treatment_id):
#     """ Preprocess data based on treatment id
# 
#     Args:
#         data: data from model output
#         liquid: liquid object
#         treatment_id: type of treatment
#     Returns:
#         Success or not
#     """
#     success = True
#     if treatment_id == 1:
#         success = _process_speech_search(data, liquid)
#     elif treatment_id == 2:
#         success = _process_image_search(data, liquid)
#     else:
#         print("Error - treatment id not found")
#     return success
# 
# 
# def _process_speech_search(data, liquid):
#     return None
# 
# 
# def _process_image_search(data, liquid):
#     """ TODO """
#     path = s3.get_s3_liquid_path(liquid.user_id, liquid.video.id, liquid.id)
#     frames_path = f"{path}/frames"
# 
#     get_frame_time = 0
#     upload_frame_time = 0
# 
#     # use opencv (cv2) to get frames based on timestamp
#     video_capture = cv2.VideoCapture(liquid.video.url)
#     for label in data:
#         # get frame based on timestamp
#         start = time.time()
#         timestamp = label["Timestamp"]
#         video_capture.set(cv2.CAP_PROP_POS_MSEC, timestamp)
#         _, frame = video_capture.read()
#         end = time.time()
#         get_frame_time += end - start
# 
#         # save frame to s3 bucket
#         start = time.time()
#         frame_key = f"{frames_path}/{timestamp}.jpg"
#         success = s3.upload_fileobj(
#             obj=numpy_to_binary(frame),
#             key=frame_key,
#             content_type="image/jpeg"
#         )
#         if not success:
#             print(f"Error uploading {timestamp}")
#             return False
#         end = time.time()
#         upload_frame_time += end - start
# 
#         # add url to data object
#         label["FrameURL"] = s3.get_object_url(frame_key)
# 
#     key = f"{path}/data.json"
#     s3.put_object(
#         obj=json.dumps(data),
#         key=key,
#         content_type="application/json",
#     )
#     if not success:
#         print(f"Error uploading json file.")
#         return False
# 
#     print(f"Total of {get_frame_time} seconds to get frames from opencv")
#     print(f"Total of {upload_frame_time} seconds to upload frame")
# 
#     return True
# 
# 
# def numpy_to_binary(arr):
#     """ Convert the numpy array to a binary object in memory"""
#     _, buffer = cv2.imencode(".jpg", arr)
#     io_buf = io.BytesIO(buffer)
#     return io_buf
