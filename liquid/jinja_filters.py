import collections
from flask import current_app as app


@app.template_filter('render_timestamps')
def render_timestamps(data):
    return map_nested_objs(data, convert)


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def map_nested_objs(ob, func):
    """
    This function recursively  pplies `func` to each obj nested within a dictionary/array
    structure. Ex given ob [{"a": 1}, {"b": 2}], `func()` will be applied 1 and 2

    This function applies `func` in place and returns `ob`
    """
    if isinstance(ob, collections.Mapping):
        return {k: map_nested_objs(v, func) for k, v in ob.items()}
    elif isinstance(ob, collections.Iterable):
        return [map_nested_objs(v, func) for v in ob]
    else:
        return func(ob)
