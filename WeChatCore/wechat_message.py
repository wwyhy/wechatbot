from wcferry import WxMsg
from wcferry import wcf_pb2


class WeChatMessage(WxMsg):
    def __init__(self, msg: wcf_pb2.WxMsg) -> None:
        super().__init__(msg)
