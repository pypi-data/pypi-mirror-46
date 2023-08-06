from flask import Response
import json

class RMResponse(Response):
    def __init__(self, result=None, error=None, id=None):
        obj = {'jsonrpc': '2.0'}

        if error is None:
            obj['result'] = result
            obj['id'] = id
        else:
            obj['error'] = error
            obj['id'] = None

        super().__init__(json.dumps(obj), mimetype='application/json')