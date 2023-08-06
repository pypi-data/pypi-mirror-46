from flask import Flask
from flask import request as fl_request
from .request import RMRequest, InvalidJsonError, InvalidRequestError
from .response import RMResponse
from .error import RMError
import sys
import os
import shutil
import tempfile

app = Flask('rufmich')
@app.route("/rufmich", methods=['POST'])
def rufmich():
    try:
        request = RMRequest(fl_request)
    except InvalidJsonError:
        return RMResponse(error={'code': -32700, 'message': 'Parse error'}, id=None)
    except InvalidRequestError:
        return RMResponse(error={'code': -32600, 'message': 'Invalid Request'}, id=None)

    try:
        result = request.process()
    except (ModuleNotFoundError, AttributeError):
        return RMResponse(error={'code': -32601, 'message': 'Method not found'}, id=None)
    except TypeError:
        return RMResponse(error={'code': -32602, 'message': 'Invalid params'}, id=None)
    except RMError as error:
        return RMResponse(error=error.to_dict(), id=None)
    except:
        return RMResponse(error={'code': -32603, 'message': 'Internal error'}, id=None)

    return RMResponse(result=result, id=None)

class RMServer():
    def __init__(self, load_path):
        self.load_path = load_path
    
    def run(self, **kw):
        with tempfile.TemporaryDirectory() as temp_dir:
            work_dir = os.path.join(temp_dir, 'methods')
            shutil.copytree(self.load_path, work_dir)
            sys.path.insert(0, work_dir)
            app.run(**kw)