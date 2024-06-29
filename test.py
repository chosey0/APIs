import os

from interface.base.messages_factory import BaseMessage
print(BaseMessage.from_kwargs(tr_id="test").to_dict())