# throttled-socket
This is simple wrapper that allows rate limiting reads/writes on a socket.

## Usage
The usage is pretty simple, simply create a socket like you have always done and pass it to a new `ThrottledSocket` object. `ThrottledSocket` object will use the original socket for all read/write calls while making sure the data flow rate does not exceed the value you decide.

Example:
```python
import socket

from throttledsocket.socketwrapper import ThrottledSocket

orig_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig_sock.connect(('127.0.0.1', 1234))

# We will use the original socket here to transfer data at 2 bytes/second.
throttled_sock = ThrottledSocket(test_sock, 2)
throttled_sock.write('some data to be transferred')
```

Of course, there is a `read` method as well which works in the same way :)
