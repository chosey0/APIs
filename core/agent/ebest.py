import os
import requests
from typing import Dict, Any, Tuple

from interface.base.agent import AgentInterface
from interface.eBest.messages import GetTokenMessage
from datetime import datetime, timedelta

import logging

logger = logging.getLogger(__name__)

class eBestAgent(AgentInterface):
    name = "EBEST"
    
    @classmethod
    def get_token(cls) -> Dict[str, str]:
        try:
            response = requests.post(**GetTokenMessage().to_dict())
            response_json = response.json()
            response.raise_for_status()
            return cls.parsing_token_exp(response_json)
        
        except Exception as e:
            logger.error(f"eBestAgent.get_token() Failed to get token")
            logger.error(f"{response_json['error_code']} - {response_json['error_description']}")
    
    @staticmethod
    def parsing_token_exp(response_json: Dict[str, Any]) -> Tuple[str, str]:
        try:
            TOKEN = f"{response_json['token_type']} {response_json['access_token']}"
            TOKEN_EXP = datetime.strftime(datetime.now() + timedelta(seconds=int(response_json["expires_in"])), "%Y-%m-%d %H:%M:%S")
            return TOKEN, TOKEN_EXP
        except Exception as e:
            logger.error(f"eBestAgent.parsing_token_exp() Failed to parsing response JSON")
            logger.error(f"{response_json['error_code']} - {response_json['error_description']}")