import zmq
import logging
import types
from functools import wraps
from zmq.asyncio import Context
from .message import decode_msg, encode_msg, MsgPack

logger = logging.getLogger(__package__)


class SimRpcClient:
    def __init__(self, server_address="tcp://localhost:5559",
                 is_async=False, timeout=3000, msg_tool=None):
        self.is_async = is_async
        self.server_address = server_address
        self.poll = zmq.Poller()
        self.async_poll = zmq.asyncio.Poller()
        self.timeout = timeout
        msg_tool = msg_tool or MsgPack
        self.msg_tool = msg_tool()

    def get_socket(self):
        if self.is_async:
            context = Context()
        else:
            context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(self.server_address)
        self.poll.register(socket, zmq.POLLIN)
        return socket

    def task(self, response_only: bool = False, func=False):

        def decorate(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                if len(args) > 0:
                    cls = args[0]
                else:
                    cls = func
                if hasattr(cls, "__module__") and \
                        cls.__class__.__name__ != "function":
                    cls = args[0]
                    args = args[1:]
                else:
                    cls = func
                client = kwargs.pop('rpc_client', False)
                if client:
                    data = decode_msg(
                        service=cls.__class__.__name__ if cls else "",
                        entry=func.__name__,
                        args=args,
                        kwargs=kwargs
                    )
                    if hasattr(cls, "socket"):
                        socket = getattr(cls, "socket")
                    else:
                        socket = self.get_socket()
                        setattr(cls, "socket", socket)
                    try:
                        socket.send(data)
                    except Exception as tmp:
                        print("send_error", tmp)
                    socks = dict(self.poll.poll(self.timeout))
                    if socks.get(socket) == zmq.POLLIN:
                        res = socket.recv()
                    else:
                        res = b'\x82\xa8response\xc0\xa3msg\xa7timeout'
                    return self.msg_tool.encode_msg(res, response_only=response_only)
                else:
                    qual_name = func.__qualname__.split('.')
                    if len(qual_name) > 1:
                        return func(cls, *args, **kwargs)
                    else:
                        print(func, isinstance(func, types.MethodType))
                        return func(*args, **kwargs)

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                cls = args[0]
                if hasattr(cls, "__module__") and \
                        cls.__class__.__name__ != "function":
                    cls = args[0]
                    args = args[1:]
                else:
                    cls = func
                client = kwargs.get('client', False)
                if client:
                    data = self.msg_tool.decode_msg(
                        service=cls.__class__.__name__ if cls else "",
                        entry=func.__name__,
                        args=args,
                        kwargs=kwargs
                    )
                    if hasattr(cls, "socket"):
                        socket = getattr(cls, "socket")
                    else:
                        socket = self.get_socket()
                        setattr(cls, "socket", socket)
                    await socket.send(data)
                    socks = await self.async_poll.poll(self.timeout)
                    socks = dict(socks)
                    if socks.get(socket) == zmq.POLLIN:
                        res = await socket.recv()
                    else:
                        await socket.recv()
                        res = b'\x82\xa8response\xc0\xa3msg\xa7timeout'
                    return self.msg_tool.encode_msg(res, response_only=response_only)
                else:
                    qual_name = func.__qualname__.split('.')
                    if len(qual_name) > 1:
                        return await func(cls, *args, **kwargs)
                    else:
                        return await func(*args, **kwargs)

            if self.is_async:
                return async_wrapper
            else:
                return wrapper
        return decorate
