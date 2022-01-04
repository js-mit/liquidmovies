import cv2
import io


def numpy_to_binary(arr):
    """ Convert video from numpy array to a binary object in memory """
    _, buffer = cv2.imencode(".jpg", arr)
    io_buf = io.BytesIO(buffer)
    return io_buf


def get_duration_and_frame_count(video_path):
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
