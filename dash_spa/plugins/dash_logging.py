import sys
from flask import request
import re
import json
from enum import IntEnum


def printf(format, *args):
    sys.stdout.write(format % args)

from ..utils.time import time_ms

class DEBUG_LEVEL(IntEnum):
    NONE = 0
    REQUESTS = 1
    VERBOSE = 2

class DashLogger:
    """Adds request/response logging to Dash client/server communication

    Args:
        level (DEBUG_LEVEL, optional): _description_. Defaults to DEBUG_LEVEL.NONE.

    Usage:
    ```
            from dash import Dash
            from dash_spa.utils import  DashLogger, DEBUG_LEVEL

            app = Dash(__name__)

            logger=DashLogger(DEBUG_LEVEL.VERBOSE)
            logger.init(app.server)

            if __name__ == '__main__':
                app.run_server()
    ```
    """

    count = 0
    tlast = time_ms()

    def __init__(self, app, level:DEBUG_LEVEL = DEBUG_LEVEL.NONE):
        self.level = level
        self.transferred = 0

        @app.server.before_request
        def before_request_cb():
            self.count += 1
            try:

                dt = self.get_dt()
                if dt > 1000:
                    printf('[*** %sms ***]\n', dt)
                    self.transferred = 0
                    self.count = 1
                else:
                    printf('\n')

                if request.path in ['/_dash-update-component']:
                    self.dash_request_logger(request)
                else:
                    self.asset_logger(request)
            except:
                printf('Logger exception %s\n', request.path)

        @app.server.after_request
        def after_request_func(response):
            try:
                if request.path in ['/_dash-update-component']:
                    self.dash_response_logger(response)
                else:
                    count = self.count
                    self.transferred += response.content_length
                    printf('%03d res %s (%s bytes/%s total)\n', count, request.path, response.content_length, self.transferred)
            except:
                printf('Logger exception %s\n', request.path)

            return response


    def get_dt(self):
        tlast = self.tlast
        self.tlast = tnow = time_ms()
        return tnow - tlast

    def asset_logger(self, request):
        count = self.count
        printf('%03d req %s\n', count, request.path)

    def dash_request_logger(self, request):
        body = request.get_json()
        self.formatter = DebugFormatter(body)

        # Create input report

        count = self.count

        if self.level > DEBUG_LEVEL.NONE:

            input_list = self.formatter.req2str()

            printf('%03d req %s\n', count, input_list)

        else:
            input_length = len(json.dumps(self.formatter.req_inputs))
            output_length = len(json.dumps(self.formatter.req_output))
            printf('%03d req %d bytes\n', count, input_length + output_length)


    def dash_response_logger(self, response):
        count = self.count
        self.transferred += response.content_length

        if self.level > DEBUG_LEVEL.NONE:
            element_list = self.formatter.outputs2str(response)
            printf('%03d res %s', count, element_list)
        else:
            printf('%03d res', count)

        printf(' (%s bytes/%s total)\n', response.content_length, self.transferred)

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

        inputs = self.req_inputs
        if isinstance(inputs[0], list):
            inputs = inputs[0]

        for input in inputs:
            if not isinstance(input, dict): continue
            s = f"{input['id']}.{input['property']}"
            if 'value' in input:
                s += f":\"{input['value']}\""
            input_list.append(s)

        input_list = '\n        '.join(input_list)

        outputs = re.sub(r'\.\.\.', ', ', self.req_output)
        outputs = re.sub(r'\.\.', '', outputs)

        return f'{input_list} -> [{outputs}]'


    def outputs2str(self, response):

        response = json.loads(response.data, encoding="utf-8")['response']

        # log.info('resp=%s', json.dumps(resp))

        outputs = re.sub(r'\.\.\.', ', ', self.req_output)
        outputs = re.sub(r'\.\.', '', outputs)
        outputs = outputs.split(', ')

        element_list = []
        output_index = 0

        for key, output in response.items():
            attr_list = []

            for attr, value in output.items():
                if attr == 'children':
                    value = 'markup ...'
                attr_list.append(f'"{value}"')

            attr_values = ', '.join(attr_list)
            element_list.append(f'{attr_values} -> {outputs[output_index]}')
            output_index += 1

        # switch="admin#login" -> spa#router.switch, title="Dash/SPA:Admin login" -> spa#title.title

        element_list = ', '.join(element_list)

        return element_list


def plug(app):
    logger = DashLogger(app, level=DEBUG_LEVEL.VERBOSE)
