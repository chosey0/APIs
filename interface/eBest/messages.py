import os
from urllib.parse import urljoin
from dataclasses import dataclass

from interface.eBest.tr_code import TRCode
from interface.eBest.endpoint import Endpoint
from interface.base.messages_factory import MessageStrategy, BaseMessage, Header, Body

class GetToken(MessageStrategy):
    @staticmethod
    def create_message(**kwargs) -> BaseMessage:
        url = urljoin(Endpoint.base_url, Endpoint.get_token)
        headers = Header(content_type="application/x-www-form-urlencoded").to_dict()
        data = Body(grant_type="client_credentials",
                    appkey=os.getenv("EBEST_RAPP"),
                    appsecretkey=os.getenv("EBEST_RSEC"),
                    scope="oob").to_dict()
        return BaseMessage(url=url, headers=headers, data=data).to_dict()
