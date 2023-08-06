# Rufmich
A Python server implementaion of [JSON-RPC 2.0](https://www.jsonrpc.org/specification) over HTTP.

## Introduction
**rufmich** is an HTTP server for JSON-RPC 2.0. To make the JSON-RPC 2.0 work over HTTP, following specifications are added:

1. The transport protocol is HTTP. The response for an notification is an HTTP response with status code 204 (No Response) and empty content. The HTTP requests must have the header `content-type: application/json`, otherwise there will be an HTTP error 415 (Unsupported Media Type).
2. A notification request will get an immediate response. Usually the server will start the procedure and return the response immediately (without having to wait for the procedure to finish). And there is no callback for the procedure, which means the client would not be aware of any errors.
3. Method namespacing is supported (and recommended).

### Notification
Notification is implemented using threading. A method without `id` will be invoked in a new thread.

### Batch
If multiple requests are sent in a batch, they will be processed concurrently by a thread pool.

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

### Run
```python
from rufmich.server import RMServer

server = RMServer(load_path=<your_methods_workspace>)
server.run(port=<port>)
```

### Client examples
Check on [the website of JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification#examples).