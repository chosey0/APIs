import os
from urllib.parse import urljoin
from dataclasses import dataclass

from interface.kis.tr_code import TRCode
from interface.kis.endpoint import Endpoint
from interface.base.messages_factory import BaseMessage, Header, Body

@dataclass
class GetApprovalMessage(BaseMessage):
    def __init__(self):
        url = urljoin(Endpoint.base_url, Endpoint.approval_key)
        headers = Header().to_dict()
        data = Body(grant_type="client_credentials",
                    appkey=os.getenv("KIS_RAPP"),
                    secretkey=os.getenv("KIS_RSEC")).to_json()
        super().__init__(url, headers, data=data)
        
@dataclass
class GetTokenMessage(BaseMessage):
    def __init__(self):
        url = urljoin(Endpoint.base_url, Endpoint.get_token)
        headers = Header().to_dict()
        json = Body(grant_type="client_credentials",
                    appkey=os.getenv("KIS_RAPP"),
                    appsecret=os.getenv("KIS_RSEC")).to_dict()
        super().__init__(url, headers, json=json)
        
@dataclass
class SubscribeMessage(BaseMessage):
    def __init__(self, approval_key: str, stock_code: str, tr_id: str):
        headers = {
            "approval_key": approval_key,
            "custtype": "P",
            "tr_type": TRCode.subscribe,
            "Content-Type": "utf-8"
        }
        body = {
            "input": {
                "tr_id": tr_id,
                "tr_key": stock_code
            }
        }
        super().__init__(headers=headers, body=body)
        
@dataclass
class UnsubscribeMessage(BaseMessage):
    def __init__(self, approval_key: str, stock_code: str, tr_id: str):
        headers = {
            "approval_key": approval_key,
            "custtype": "P",
            "tr_type": TRCode.unsubscribe,
            "Content-Type": "utf-8"
        }
        body = {
            "input": {
                "tr_id": tr_id,
                "tr_key": stock_code
            }
        }
        super().__init__(headers=headers, body=body)
