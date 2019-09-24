import os
import re
import flask
import json
import dash
from enum import IntEnum

from .printf import printf
from .time import time_ms


class DEBUG_LEVEL(IntEnum):
    NONE = 0
    REQUESTS = 1
    VERBOSE = 2

DASH_DEBUG = int(os.environ.get('DASH_DEBUG', 0))

class DebugFormatter:

    def __init__(self, req):
        self.req_inputs = req.get('inputs', [])
        self.req_output = req['output']

        # log.info('req_inputs=%s', json.dumps(self.req_inputs))
        # log.info('req_output=%s', json.dumps(self.req_output))


    def req2str(self):
        """Convert request inputs dictionary into a string for display

        Typical input list:

            [
                {'id': 'test#page1#btn', 'property': 'n_clicks', 'value': 1}
                {'id': 'test#redirect', 'property': 'href', 'value': '/test/route'}
            ]

        Output

            test#page1#btn.n_clicks="1", test#redirect.href="/test/route"

        Arguments:
            req_inputs {list} -- List of input attributes and associated values

        Returns:
            str -- String for display
        """

        input_list = []
        for input in self.req_inputs:
            s = '{}.{}'.format(input['id'], input['property'])
            if 'value' in input:
                s += ':"{}"'.format(input['value'])
            input_list.append(s)

        input_list = ', '.join(input_list)

        outputs = re.sub(r'\.\.\.', ', ', self.req_output)
        outputs = re.sub(r'\.\.', '', outputs)

        return '{} -> [{}]'.format(input_list, outputs)


    def outputs2str(self, resp):

        resp = json.loads(resp.data, encoding="utf-8")['response']

        # log.info('resp=%s', json.dumps(resp))

        outputs = re.sub(r'\.\.\.', ', ', self.req_output)
        outputs = re.sub(r'\.\.', '', outputs)
        outputs = outputs.split(', ')

        element_list = []
        output_index = 0

        for key, output in resp.items():
            attr_list = []

            for attr, value in output.items():
                attr_list.append('"{}"'.format(value))

            attr_values = ', '.join(attr_list)
            element_list.append('{} -> {}'.format(attr_values, outputs[output_index]))
            output_index += 1

        # switch="admin#login" -> spa#router.switch, title="Dash/SPA:Admin login" -> spa#title.title

        element_list = ', '.join(element_list)

        return element_list



class DashDebug(dash.Dash):

    count = 0
    tlast = time_ms()

    def get_index(self):
        count = DashDebug.count + 1
        DashDebug.count = count
        return count

    def get_dt(self):
        tlast = DashDebug.tlast
        DashDebug.tlast = tnow = time_ms()
        return tnow - tlast


    def dispatch(self):
        """_dash-update-component
        
        Returns:
            [type] -- [description]
        """

        body = flask.request.get_json()
        formatter = DebugFormatter(body)

        # Create input report

        count = self.get_index()

        if DASH_DEBUG > DEBUG_LEVEL.NONE:

            input_list = formatter.req2str()

            if self.get_dt() > 1000:
                printf('\n')

            printf('%03d req %s\n', count, input_list)

        else:
            input_length = len(json.dumps(formatter.req_inputs))
            output_length = len(json.dumps(formatter.req_output))
            printf('%03d req %d bytes\n', count, input_length + output_length)


        # Process the inputs

        try:
            resp = super().dispatch()
        except dash.exceptions.PreventUpdate as ex:
            printf('%03d res NOACTION\n', count)
            raise ex

        # Create response report

        if DASH_DEBUG > DEBUG_LEVEL.NONE:

            element_list = formatter.outputs2str(resp)
            printf('%03d res %s\n', count, element_list)

        else:
            printf('%03d res %d bytes\n', count, len(resp.data))


        return resp

    def dependencies(self):
        """_dash-dependencies
        
        Returns:
            [type] -- [description]
        """

        resp = super().dependencies()

        count = self.get_index()
        tmp = json.loads(resp.data, encoding="utf-8")

        if DASH_DEBUG == DEBUG_LEVEL.VERBOSE:

            printf('%03d _dash-dependencies %s\n', count, json.dumps(tmp, indent=2))
        else:
            printf('%03d _dash-dependencies %d bytes\n', count, len(resp.data))

        return resp

    def serve_layout(self):
        """_dash-layout

        Returns:
            [type] -- [description]
        """

        resp = super().serve_layout()

        count = self.get_index()
        tmp = json.loads(resp.data, encoding="utf-8")

        if DASH_DEBUG == DEBUG_LEVEL.VERBOSE:
      
            printf('%03d _dash-layout %s\n', count, json.dumps(tmp, indent=2))
        else:
            printf('%03d _dash-layout %d bytes\n', count, len(resp.data))

        return resp

