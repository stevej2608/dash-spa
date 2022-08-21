import re
import plotly
import json


def json_layout(layout):
    """Dump the given component layout"""

    # ReduxStore elements use a hash() to generate a component
    # id. This is a problem when testing because the hash() seed changes
    # on each test run. Here we pick out the hash based ids' and replace
    # them with an index.

    id_list = []

    def replace_id(match):
        val = match.group(0).split(': ')[1]
        if val not in id_list:
            id_list.append(val)
        return f"\"idx\": \"PYTEST_REPLACEMENT_ID_{id_list.index(val)}\""

    # "idx": "2438d368d91cd816"

    json_str = json.dumps(layout, indent=2, cls=plotly.utils.PlotlyJSONEncoder)
    json_str = re.sub(r'\"idx\": \"[0-9a-f]+\"', replace_id, json_str)

    # json_str = re.sub(r': true', ': True', json_str)
    # json_str = re.sub(r': false', ': False', json_str)
    json_str = re.sub(r': null', ': []', json_str)

    return json_str


def dumps_layout(layout):
    json_str = json_layout(layout)
    return json.loads(json_str)
