""" Consider renaming this file or reorganizing the functions within it """
from typing import Mapping, Iterable, Union


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
    elif treatment_id == 4:
        results = _render_diarization(data)
    else:
        print("Error - treatment id not found")

    return results


def _render_speech_search(data):
    # TODO
    return data


def _render_image_search(data):
    # TODO
    return data


def _render_text_search(data):
    # TODO
    return data


def _render_diarization(data: Union[Mapping, Iterable]) -> Union[Mapping, Iterable]:
    """
    returns {
        "spk_0": [{
            "start_time": 1,
            "end_time": 3,
        }, ...],
        "spk_1": [{...}],
    }
    """
    ret = {}
    num_speakers = data["results"]["speaker_labels"]["speakers"]
    segments = data["results"]["speaker_labels"]["segments"]

    for segment in segments:
        speaker = segment["speaker_label"]
        start_end_dict = {
            "start_time": int(float(segment["start_time"])*1000),
            "end_time": int(float(segment["end_time"])*1000),
        }
        if speaker in ret:
            ret[speaker].append(start_end_dict)
        else:
            ret[speaker] = [start_end_dict]
    return ret
