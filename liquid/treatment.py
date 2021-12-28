""" Consider renaming this file or reorganizing the functions within it """
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
