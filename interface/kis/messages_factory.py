from typing import Any

from interface.base.messages_factory import MessageFactory
from interface.kis.messages import create_subscribe_message

class KIS_MessageFactory(MessageFactory):
    @staticmethod
    def create_message(message_type: str, **kwargs) -> Any:
        if message_type == "subscribe":
            return create_subscribe_message(kwargs.get("stock_code"), kwargs.get("tr_id"))
        else:
            raise ValueError(f"Unknown message type: {message_type}")
