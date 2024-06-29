import os
import json
import asyncio
import requests
from datetime import datetime
from websockets import WebSocketClientProtocol
from typing import Optional, Dict, Any, Tuple

from interface.base.agent import AgentInterface
from interface.kis.messages import GetApprovalMessage, GetTokenMessage

import logging

# Set up logging
logger = logging.getLogger(__name__)

class KISAgent(AgentInterface):
    name = "KIS"
    
    @classmethod
    def get_token(cls) -> Dict[str, str]:
        try:
            response = requests.post(**GetTokenMessage().to_dict())
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
            response = requests.post(**GetApprovalMessage().to_dict())
            response_json = response.json()
            
            if response.status_code == 200:
                logger.info(f"KISAgent.get_approval_key() {response.status_code} - Successfully got websocket key")
            else:
                logger.error(f"KISAgent.get_approval_key() {response.status_code} - {response_json['error_description']}")
                raise Exception(f"Failed to get_approval_key() {response.status_code}")
            
            return response_json["approval_key"]
        
        except Exception as e:
            logger.error(e)
    
    @staticmethod
    async def send_websocket_msg(session: WebSocketClientProtocol, senddata: Dict[str, Any]):
        """_summary_
            현재 연결된 웹소켓 세션에 구독 및 해제 요청 메세지 전송 메소드

        Args:
            session (WebSocketClientProtocol): 현재 연결된 웹소켓 세션
            senddata (Dict[str, Any]): 전송할 JSON String
        """
        await session.send(json.dumps(senddata))
        await logger.info(f"KISAgent.send_subscribe_msg() - {json.dumps(senddata)['body']['input']['tr_key']}")