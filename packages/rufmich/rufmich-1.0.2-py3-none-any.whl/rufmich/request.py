import importlib
from .response import RMResponse, RMResponseNone, RMResponseList
from .error import RMError
from multiprocessing.pool import ThreadPool
import threading

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

    if isinstance(arg, list):
        return f(*arg)
    elif isinstance(arg, dict):
        return f(**arg)
    else:
        # <unpredicted error>
        # if the arg bypassed the sanity check, its
        # type should be list or dict
        raise Exception

class RMRequest:
    def __init__(self, fl_request):
        self.obj = fl_request.get_json(silent=True)

    def process(self):
        if self.obj is None:
            return RMResponse(error={'code': -32700, 'message': 'Parse error'}, id=None)

        if isinstance(self.obj, list):
            obj_list = self.obj
            size = len(obj_list)
            if size == 0:
                return RMResponse(error={'code': -32600, 'message': 'Invalid Request'}, id=None)

            pool = ThreadPool(size)
            results = []
            for obj in obj_list:
                results.append(pool.apply_async(self.process_one, args=(obj,)))
            pool.close()
            pool.join()

            results = [r.get() for r in results]
            return RMResponseList(results)
        else:
            return self.process_one(self.obj)

    def process_one(self, obj):
        try:
            self.sanity_check(obj)

            if 'id' in obj:
                result = invoke_method(obj['method'], obj.get('params', []))
                return RMResponse(result=result, id=obj['id'])
            else:
                # Notification
                t = threading.Thread(target=invoke_method, args=(obj['method'], obj.get('params', [])))
                t.start()
                return RMResponseNone()

        except InvalidRequestError:
            return RMResponse(error={'code': -32600, 'message': 'Invalid Request'}, id=None)
        except (ModuleNotFoundError, AttributeError):
            return RMResponse(error={'code': -32601, 'message': 'Method not found'}, id=obj['id'])
        except TypeError:
            return RMResponse(error={'code': -32602, 'message': 'Invalid params'}, id=obj['id'])
        except RMError as error:
            return RMResponse(error=error.to_dict(), id=obj['id'])
        except:
            return RMResponse(error={'code': -32603, 'message': 'Internal error'}, id=None)

    def sanity_check(self, obj):
        try:
            assert isinstance(obj, dict)
            assert obj['jsonrpc'] == '2.0'
            assert isinstance(obj['method'], str)
            if 'params' in obj:
                assert isinstance(obj['params'], list) \
                    or isinstance(obj['params'], dict)
            if 'id' in obj:
                assert isinstance(obj['id'], str) \
                    or isinstance(obj['id'], int) \
                    or obj['id'] is None
        except:
            raise InvalidRequestError