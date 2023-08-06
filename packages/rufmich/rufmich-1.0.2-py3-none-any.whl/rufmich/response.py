from flask import Response
import json

class RMResponseNone(Response):
    def __init__(self):
        super().__init__('', status=204, mimetype='application/json')

class RMResponse(Response):
    def __init__(self, result=None, error=None, id=None, empty=False):
        self.obj = {'jsonrpc': '2.0'}
        self.obj['id'] = id

        if error is None:
            self.obj['result'] = result
        else:
            self.obj['error'] = error

        super().__init__(json.dumps(self.obj), mimetype='application/json')

    def to_dict(self):
        return self.obj

class RMResponseList(Response):
    def __init__(self, response_list):
        res = []
        for response in response_list:
            if isinstance(response, RMResponse):
                res.append(response.to_dict())

        if len(res) > 0:
            super().__init__(json.dumps(res), mimetype='application/json')
        else:
            super().__init__('', status=204, mimetype='application/json')





    
        