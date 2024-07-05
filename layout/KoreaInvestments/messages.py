import os

import pandas as pd
from datetime import datetime

from urllib.parse import urljoin
from typing import Dict

from layout.KoreaInvestments.tr_code import TRCode
from layout.KoreaInvestments.endpoint import Endpoint
from interface.messages_factory import MessageStrategy, BaseMessage

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

class OverseasDayCandle(MessageStrategy):
    @staticmethod
    def create_message(
                        symbol, 
                        tr_cont: str = "", 
                        exchange_code: str = "NAS", 
                        gap_distinction: int = 0, 
                        find_by_date: datetime = datetime.today(),
                        KEYB: str = "") -> BaseMessage:

        url = urljoin(Endpoint.base_url, Endpoint.overseas_day_candle)
        headers = BaseMessage.from_kwargs(
                        authorization=os.getenv("KIS_TOKEN"),
                        appkey=os.getenv("KIS_RAPP"),
                        appsecret=os.getenv("KIS_RSEC"),
                        content_type="application/json; charset=utf-8",
                        tr_id=TRCode.overseas_day_candle,
                        tr_cont=tr_cont,
                        custtype="P",
                        ).to_dict()

        params = BaseMessage.from_kwargs(
            AUTH="",
            EXCD=exchange_code,
            SYMB=symbol,
            GUBN=f"{gap_distinction}",
            BYMD=find_by_date.strftime("%Y%m%d"),
            MODP="1", # 수정주가반영여부
            KEYB=KEYB
            ).to_dict()
        
        return BaseMessage.from_kwargs(url=url, headers=headers, params=params).to_dict()
    
    @staticmethod
    def handler(data):
        
        df = pd.DataFrame(data["output2"]).iloc[::-1].reset_index(drop=True)
        df["time"] = pd.to_datetime(df["xymd"], format="%Y%m%d")
        df.drop(labels=["xymd", "sign", "diff", "rate", "pbid", "vbid", "pask", "vask"], axis=1, inplace=True)
        
        df.rename(columns={"tvol": "volume", "tamt": "amount", "clos": "close"}, inplace=True)
        df = df[["time", "open", "high", "low", "close", "volume", "amount"]]
        df.set_index("time", inplace=True)
        
        return df
    
class OverseasMinuteCandle(MessageStrategy):
    @staticmethod
    def create_message(symbol, tr_cont: str = "", exchange_code: str = "NAS", gap: int = 1) -> BaseMessage:
        url = urljoin(Endpoint.base_url, Endpoint.overseas_minute_candle)
        headers = BaseMessage.from_kwargs(
                        content_type="application/json; charset=utf-8",
                        authorization=os.getenv("KIS_TOKEN"),
                        appkey=os.getenv("KIS_RAPP"),
                        appsecret=os.getenv("KIS_RSEC"),
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
    
    @staticmethod
    def handler(data):
        
        df = pd.DataFrame(data["output2"]).iloc[::-1].reset_index(drop=True)
        df["time"] = pd.to_datetime(df["xymd"] + df["xhms"], format="%Y%m%d%H%M%S")
        df.drop(labels=["tymd", "xymd", "xhms", "kymd", "khms"], axis=1, inplace=True)
        
        df.rename(columns={"evol": "volume", "eamt": "amount", "last": "close"}, inplace=True)
        df = df[["time", "open", "high", "low", "close", "volume", "amount"]]
        df.set_index("time", inplace=True)
        
        return df

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