import msgpack
import uuid
import logging

logger = logging.getLogger(__package__)


class BaseMsg:
    def __init__(self, name=None):
        self.name = name

    def decode_msg(self, *args, **kwargs):
        raise NotImplementedError

    def encode_msg(self, *args, **kwargs):
        raise NotImplementedError

    def decode_msg_body(self, *args, **kwargs):
        raise NotImplementedError


class MsgPack(BaseMsg):
    def __init__(self, name=None):
        self.name = name or 'msg_pack'

    def decode_msg(self, service=None, entry=None, args=None, kwargs=None):
        data = {
            "service": service,
            "entry": entry,
            "args": args,
            "kwargs": kwargs,
            "id": str(uuid.uuid1()),
            "response": None
        }
        logger.debug(data)
        data_sent = msgpack.dumps(data)
        return data_sent

    def encode_msg(self, data, response_only: bool = False):
        res = msgpack.loads(data, encoding='utf-8')
        if response_only:
            return res.get("response", {})
        else:
            return res

    def decode_msg_body(self, data):
        return msgpack.dumps(data)
