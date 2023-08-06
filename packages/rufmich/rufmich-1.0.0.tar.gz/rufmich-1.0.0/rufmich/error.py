class RMError(Exception):
    def __init__(self, eid, message, data=None):
        self.obj = {
            'code': -32000 - eid,
            'message': message,
            'data': data
        }

    def to_dict(self):
        return self.obj