from abc import ABC, abstractmethod
import os
from dotenv import find_dotenv, set_key

import websockets
from websockets import WebSocketClientProtocol

import asyncio
from datetime import datetime

from typing import Dict, Tuple
from dataclasses import dataclass

import logging
import requests

# Set up logging
logger = logging.getLogger(__name__)

class AgentInterface(ABC):
    
    @staticmethod
    def get(url, headers, params):
        response = requests.get(url=url, headers=headers, params=params)
        
        try:
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"[AgentInterface.get] HTTP Error")
            logger.error(f"{response.json()['msg_cd']} - {response.json()['msg1']}")
    
    @staticmethod
    @abstractmethod
    def parsing_token_exp(response_json: Dict[str, str]) -> Tuple[str, str]:
        """_summary_

        Args:
            response_json (Dict[str, str]): 각 증권사 별 토큰 발급 요청에 대한 응답 Dict

        Raises:
            NotImplementedError: 각 증권사 별 토큰 발급 응답에 대한 처리 로직 구현 필요.

        Returns:
            Tuple[str, str]: TOKEN, TOKEN_EXP
        """
        
        raise NotImplementedError
    
    @abstractmethod
    def get_token() -> Dict[str, str]:
        """_summary_
            RestAPI 요청을 위해 토큰 발급을 요청하는 추상 클래스 메소드
            
        Returns:
            Dict[str, str]: TOKEN, TOKEN_EXP
        """
        raise NotImplementedError
    
    @classmethod
    def read_token(cls) -> str:
        """_summary_
            현재 클래스의 name 속성에 따라 환경 변수에서 토큰을 읽어온다.
            토큰이 없거나 유효 기간이 만료되었을 경우, update_token 메소드를 호출하여 토큰을 갱신한다.

        Returns:
            str: Access Token
        """
        TOKEN = os.getenv(f"{cls.name}_TOKEN")
        TOKEN_EXP = os.getenv(f"{cls.name}_TOKEN_EXP")
        
        if TOKEN is None or TOKEN == "":
            logger.info("Token is not set or expired. Requesting new token...")
            TOKEN = cls.update_token()

        elif (datetime.strptime(TOKEN_EXP, "%Y-%m-%d %H:%M:%S") - datetime.now()).total_seconds() < 0:
            logger.info("Token is expired. Updating token...")
            TOKEN = cls.update_token()
        
        return TOKEN
    
    @classmethod
    def update_token(cls) -> str:
        """_summary_
            환경 변수에 저장된 토큰과 토큰 만료 시간을 갱신.
            cls.get_token: 토큰을 발급하는 클래스 메소드

        Returns:
            str: TOKEN
        """
        try:
            dotenv_file = find_dotenv()
            if not dotenv_file:
                raise FileNotFoundError("'.env' file not found.")
            
            TOKEN, TOKEN_EXP = cls.get_token()
            
            set_key(dotenv_file, f"{cls.name}_TOKEN", TOKEN)
            set_key(dotenv_file, f"{cls.name}_TOKEN_EXP", TOKEN_EXP)
        except Exception as e:
            logger.error(f"[interface.agent.py - update_token] Failed to update token: {e}")
            
        return TOKEN