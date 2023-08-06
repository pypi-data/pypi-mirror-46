import importlib

class InvalidJsonError(Exception):
    pass

class InvalidRequestError(Exception):
    pass

def parse_method(method_path):
    tokens = method_path.split('::')
    if tokens[0] == '':
        tokens = tokens[1:]

    method_name = tokens[-1]
    if len(tokens) == 1:
        mod_path = '.root'
    else:
        namespace = '.'.join(tokens[:-1])
        mod = tokens[-2]
        mod_path = ".%s.%s" % (namespace, mod)

    return mod_path, method_name

def invoke_method(method_path, arg):
    mod_path, method_name = parse_method(method_path)

    mod = importlib.import_module(mod_path, 'root')
    f = getattr(mod, method_name)

    return f(*arg)

class RMRequest:
    def __init__(self, fl_request):
        self.obj = fl_request.get_json(force=True, silent=True)

        if self.obj is None:
            raise InvalidJsonError
        
        try:
            assert self.obj['jsonrpc'] == '2.0'
            assert isinstance(self.obj['method'], str)
            if 'params' in self.obj:
                assert isinstance(self.obj['params'], list)
        except Exception:
            raise InvalidRequestError
    
    def process(self):
        if 'params' in self.obj:
            return invoke_method(self.obj['method'], self.obj['params'])
        else:
            return invoke_method(self.obj['method'], [])