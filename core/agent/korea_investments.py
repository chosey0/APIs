import os

import json
import requests
from datetime import datetime, timezone
import websockets

from typing import Dict, Any, Tuple, Callable

from interface.agent import AgentInterface
from interface.websocket_agent import WebsocketAgent
from interface.message_queue import MessageQueueManager
from interface.exceptions import PingPongException, NotDataStringException
from layout.KoreaInvestments.messages import GetApproval, GetToken


import logging

logger = logging.getLogger(__name__)

class KISAgent(AgentInterface):
    name = "KIS"
    
    @classmethod
    def get_token(cls) -> Dict[str, str]:
        try:
            response = requests.post(**GetToken.create_message())
            response_json = response.json()
            response.raise_for_status()
            return cls.parsing_token_exp(response_json)
            
        except Exception as e:
            logger.error(f"[AgentInterface.get_token] Failed to get token")
            logger.error(f"{response_json['error_code']} - {response_json['error_description']}")

    @staticmethod
    def parsing_token_exp(response_json: Dict[str, Any]) -> Tuple[str, str]:
        try:
            TOKEN = f"{response_json['token_type']} {response_json['access_token']}"
            TOKEN_EXP = response_json["access_token_token_expired"]
            return TOKEN, TOKEN_EXP

        except Exception as e:
            logger.error(f"[core.agent.korea_investments.py - parsing_token_exp] Failed to parsing response JSON")
            logger.error(f"{response_json['error_code']} - {response_json['error_description']}")

    @staticmethod
    def get_approval_key() -> Dict[str, str]:
        try:
            response = requests.post(**GetApproval.create_message())
            response_json = response.json()
            
            if response.status_code == 200:
                logger.info(f"KISAgent.get_approval_key() {response.status_code} - Successfully got websocket key")
            else:
                logger.error(f"KISAgent.get_approval_key() {response.status_code} - {response_json['error_description']}")
                raise Exception(f"Failed to get_approval_key() {response.status_code}")
            
            return response_json["approval_key"]
        
        except Exception as e:
            logger.error(e)
            
class KISWebSocketAgent(WebsocketAgent):
    def __init__(self, tr_id = None):
        super().__init__()
        
        if tr_id is not None:
            self.url = f"ws://ops.koreainvestment.com:21000/tryitout/{tr_id}"
        else:
            self.url = "ws://ops.koreainvestment.com:21000"
    
    async def recv_handler(self, callback: Callable):
        recv_time = datetime.now(tz=timezone.utc).timestamp()
        recvstr = await self.session.recv()
        
        if recvstr[0] == "0":
            await callback([recv_time, recvstr])
            print(recvstr)
            return
            # status_code, tr_id, cnt, datastr = recvstr.split("|")
        else:
            raise NotDataStringException(recvstr)
    
    def not_data_string_exception_handler(self, data: str):
        jsonObject = json.loads(data)
        trid = jsonObject["header"]["tr_id"]
        
        if trid != "PINGPONG":
            rt_cd = jsonObject["body"]["rt_cd"]
            
            if rt_cd == '1':  # 에러
                if jsonObject["body"]["msg1"] != 'ALREADY IN SUBSCRIBE':
                    logger.error("### ERROR RETURN CODE [ %s ][ %s ] MSG [ %s ]" % (jsonObject["header"]["tr_key"], rt_cd, jsonObject["body"]["msg1"]))
                
            elif rt_cd == '0':  # 정상
                pass
            
        elif trid == "PINGPONG":
            raise PingPongException(data)
        
    async def receive_loop(self, callback: Callable):
        await self.connect()
        
        try:
            while True:
                try:
                    await self.recv_handler(callback)
                    
                except NotDataStringException as e:
                    try:
                        self.not_data_string_exception_handler(e.message)
                        continue
                    
                    except PingPongException as e:
                        logger.info(f"[POINPONG]{e.message}")
                        await self.session.pong(e.message)
                        continue

        except websockets.ConnectionClosed:
            print("Connection closed")

