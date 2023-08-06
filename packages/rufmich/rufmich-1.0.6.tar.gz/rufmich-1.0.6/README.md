# Rufmich
A Python server implementaion of [JSON-RPC 2.0](https://www.jsonrpc.org/specification) over HTTP.

## Introduction
**rufmich** is an HTTP server for JSON-RPC 2.0. To make the JSON-RPC 2.0 work over HTTP, following specifications are added:

1. The transport protocol is HTTP. The response for an notification is an HTTP response with status code 204 (No Response) and empty content. The HTTP requests must have the header `content-type: application/json`, otherwise there will be an HTTP error 415 (Unsupported Media Type).
2. A notification request will get an immediate response. Usually the server will start the procedure and return the response immediately (without having to wait for the procedure to finish). And there is no callback for the procedure, which means the client would not be aware of any errors.
3. Method namespacing is supported (and recommended).

### Notification
Notification is implemented using threading. A method without `id` will be invoked asynchronously in a new thread and the client will get an HTTP response with status code 204 after the creation of the thread.

### Batch
If multiple requests are sent in a batch, they will be processed concurrently by a thread pool. Only results of non-notification requests are returned. In case of that all the requests are notifications, the HTTP response will be of status 204.

## User Guide
### Installation
`pip install rufmich`

### Define methods
Create a folder with following structure:
```
- <your_methods_workspace>
    - root
        root.py
        - <A>
            <A.py>
            - <B>
                <B.py>
        - <C>
            <C.py>
```

An example is:
```
- my_methods
    - root
        root.py
        - registration
            registration.py
            - by_email
                by_email.py
```

*Note that there MUST BE a directory named root under your workspace folder.*

Each namespace folder MUST HAVE a `.py` file with the same name as the folder. The methods defined in those `.py` files will be indexed according to the folder hierarchy.

Examples:
1. A method `foobar` defined in `root.py` is indexed to `"foobar"` and `"::foobar"`
2. A method `send_code_to_email` defined in `by_email.py` in the above example is indexed to `"registration::by_email::send_code_to_email"` (and `"::registration::by_email::send_code_to_email"`)

### Application-specific errors
The error codes from -32000 to -32099 are reserved for implementation-defined server-errors. The RPC server developer can raise an application-specific error by using `RMError`:

```python
from rufmich.error import RMError

def division(a, b):
    if b == 0:
        raise RMError(eid=0, message='divided by 0', data=[a, b])
    return a / b
```

Each application-specific error should have an unique error id `eid` (0 <= eid <= 99). The error is mapped to [-32000, -32099] by the function `f: eid -> -32000-eid`.

### Run
```python
from rufmich.server import RMServer

server = RMServer(load_path='/workspace/methods')
server.run(endpoint='/jsonrpc', port=8080)
```

### Client examples
Check on [the website of JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification#examples).