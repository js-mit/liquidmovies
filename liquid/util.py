import numpy as np
from io import BytesIO
import cv2


def numpy_to_binary(arr: np.ndarray) -> BytesIO:
    """Convert video from numpy array to a binary object in memory

    Args:
        arr: numpy array representing the image
    Returns:
        Image as bytes
    """
    _, buffer = cv2.imencode(".jpg", arr)
    io_buf = BytesIO(buffer)
    return io_buf


def time_into_milliseconds(time_string):
    """Utility function to turn time string into milliseconds from H:M:S.f format."""
    hours = int(time_string[:2])
    mins = int(time_string[3:5])
    seconds = float(time_string[6:])
    return int(hours * 3600000 + mins * 60000 + seconds * 1000)


def get_duration_and_frame_count(video_path: str) -> [int, int]:
    """Get duration and frame from video using opencv

    TODO: consider switching to using cv2.CAP_PROP_POS_MSEC
    (https://stackoverflow.com/questions/49048111/how-to-get-the-duration-of-video-using-cv2)

    Args:
        video_path: path to video (can be a url)
    Returns:
        duration, frame_count
    """
    capture = cv2.VideoCapture(video_path)
    fps = capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps * 1000
    capture.release()

    return duration, frame_count
