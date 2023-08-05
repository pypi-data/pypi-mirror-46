import arrow
import json


def now():
    return arrow.utcnow()


def default_json(obj):
    if isinstance(obj, set):
        return list(obj)
    else:
        return str(obj)


def json_dumps(obj, **kwargs):
    kwargs.setdefault('indent', '  ')
    kwargs.setdefault('default', default_json)
    return json.dumps(obj, **kwargs)
