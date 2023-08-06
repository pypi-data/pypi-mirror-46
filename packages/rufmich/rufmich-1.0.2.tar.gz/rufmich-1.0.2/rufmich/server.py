from flask import Flask
from flask import request as fl_request
from flask import Response
from .request import RMRequest
import sys
import os
import shutil
import tempfile

app = Flask('rufmich')
@app.route("/rufmich", methods=['POST'])
def rufmich():
    if fl_request.content_type != 'application/json':
        return Response('', status=415, content_type='application/json')
    
    request = RMRequest(fl_request)
    return request.process()

class RMServer():
    def __init__(self, load_path):
        self.load_path = load_path
    
    def run(self, **kw):
        with tempfile.TemporaryDirectory() as temp_dir:
            work_dir = os.path.join(temp_dir, 'methods')
            shutil.copytree(self.load_path, work_dir)
            sys.path.insert(0, work_dir)
            app.run(**kw)