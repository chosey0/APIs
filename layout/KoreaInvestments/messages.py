import os
from urllib.parse import urljoin
from typing import Dict

from layout.KoreaInvestments.tr_code import TRCode
from layout.KoreaInvestments.endpoint import Endpoint
from interface.base.messages_factory import MessageStrategy, BaseMessage
    
class GetApproval(MessageStrategy):
    @staticmethod
    def create_message(**kwargs) -> BaseMessage:
        url = urljoin(Endpoint.base_url, Endpoint.approval_key)
        headers = BaseMessage.from_kwargs(content_type="application/json; utf-8").to_dict()
        data = BaseMessage.from_kwargs( grant_type="client_credentials",
                                        appkey=os.getenv("KIS_RAPP"),
                                        secretkey=os.getenv("KIS_RSEC")).to_json()
        return BaseMessage.from_kwargs(url=url, headers=headers, data=data).to_dict()

class GetToken(MessageStrategy):
    @staticmethod
    def create_message() -> BaseMessage:
        url = urljoin(Endpoint.base_url, Endpoint.get_token)
        headers = BaseMessage.from_kwargs(content_type="application/json; utf-8").to_dict()
        json = BaseMessage.from_kwargs( grant_type="client_credentials",
                                        appkey=os.getenv("KIS_RAPP"),
                                        appsecret=os.getenv("KIS_RSEC")).to_dict()

        return BaseMessage.from_kwargs(url=url, headers=headers, json=json).to_dict()

class Subscribe(MessageStrategy):
    @staticmethod
    def create_message(approval_key, tr_id, stock_code) -> BaseMessage:
        headers = BaseMessage.from_kwargs(
                        approval_key=approval_key,
                        custtype="P",
                        tr_type=TRCode.subscribe,
                        content_type="utf-8").to_dict()

        body = BaseMessage.from_kwargs(input=dict(tr_id=tr_id, tr_key=stock_code)).to_dict()
        return BaseMessage.from_kwargs(headers=headers, body=body).to_json()

class UnSubscribe(MessageStrategy):
    @staticmethod
    def create_message(approval_key, tr_id, stock_code) -> BaseMessage:
        headers = BaseMessage.from_kwargs(
                        approval_key=approval_key,
                        custtype="P",
                        tr_type=TRCode.unsubscribe,
                        content_type="utf-8").to_dict()

        body = BaseMessage.from_kwargs(
            input=BaseMessage.from_kwargs(
                tr_id=tr_id, 
                tr_key=stock_code).to_dict()
            ).to_dict()

        return BaseMessage.from_kwargs(headers=headers, body=body).to_json()

class OverseasMinuteCandle(MessageStrategy):
    @staticmethod
    def create_message(symbol, tr_cont: str = "", exchange_code: str = "NAS", gap: int = 1) -> BaseMessage:
        url = urljoin(Endpoint.base_url, Endpoint.overseas_minute_candle)
        headers = BaseMessage.from_kwargs(
                        authorization=os.getenv("KIS_TOKEN"),
                        appkey=os.getenv("KIS_RAPP"),
                        appsecret=os.getenv("KIS_RSEC"),
                        content_type="application/json; charset=utf-8",
                        tr_id=TRCode.overseas_minute_candle,
                        tr_cont=tr_cont,
                        custtype="P",
                        ).to_dict()

        params = BaseMessage.from_kwargs(
            AUTH="",
            EXCD=exchange_code,
            SYMB=symbol,
            NMIN=f"{gap}",
            PINC="1",
            NEXT="",
            NREC="120",
            FILL="",
            KEYB=""
            ).to_dict()

        return BaseMessage.from_kwargs(url=url, headers=headers, params=params).to_dict()

# headers = {
#     "approval_key": kwargs.get("approval_key"),
#     "custtype": "P",
#     "tr_type": TRCode.unsubscribe,
#     "Content-Type": "utf-8"
# }
# body = {
#     "input": {
#         "tr_id": kwargs.get("tr_id"),
#         "tr_key": kwargs.get("stock_code")
#     }
# }