from datetime import datetime, date
import json


def json_encode(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()

def json_decode(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
        except Exception:
            pass
    return json_dict

def clone(obj):
    s = json.dumps(obj, default=json_encode)
    return json.loads(s, object_hook=json_decode)