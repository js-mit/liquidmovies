""" Consider renaming this file or reorganizing the functions within it """
from typing import Mapping, Iterable, Union
from .topwords import get_topwords_for_speech_search, get_topwords_for_image_search, get_topwords_for_text_search

def render_data(
    data: Union[Mapping, Iterable], treatment_id: int
) -> Union[Mapping, Iterable]:
    """Render data for the frontend based on treatment id

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
    elif treatment_id == 3:
        results = _render_text_search(data)
    else:
        print("Error - treatment id not found")

    return results


def _render_speech_search(data):
    topwords = get_topwords(1, data)
    data['topwords'] = topwords
    return data


def _render_image_search(data):
    topwords = get_topwords(2, data)
    data['topwords'] = topwords
    return data


def _render_text_search(data):
    topwords = get_topwords(3, data)
    data['topwords'] = topwords
    return data

def get_topwords(treatment_id, data):
    if treatment_id == 1: 
        return get_topwords_for_speech_search(data)
    elif treatment_id == 2: 
        return get_topwords_for_image_search(data)
    elif treatment_id == 3: 
        return get_topwords_for_text_search(data)
    