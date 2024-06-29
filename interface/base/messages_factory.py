from typing import Dict, Any, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import json

@dataclass
class Header:
    content_type: str = "application/json; charset=UTF-8"
    approval_key: Optional[str] = None
    custtype: Optional[str] = None
    tr_type: Optional[str] = None

    def to_dict(self):
        headers = {}
        for key, value in asdict(self).items():
            if value is not None:
                headers[f'{key}'] = value
        return headers
      
    def to_json(self):
        return json.dumps(self.to_dict())
      
@dataclass
class Body:
    grant_type: Optional[str] = None
    appkey: Optional[str] = None
    appsecret: Optional[str] = None
    secretkey: Optional[str] = None
    appsecretkey: Optional[str] = None
    input: Optional[Dict[str, Any]] = None
    scope: Optional[str] = None

    def to_dict(self):
        body = {}
        for key, value in asdict(self).items():
            if value is not None:
                body[f'{key}'] = value
        return body
      
    def to_json(self):
        return json.dumps(self.to_dict())
      
@dataclass
class BaseMessage:
    url: Optional[str] = None
    headers: Optional[Dict[str, Any]] = None
    json: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None
    
    def to_dict(self):
      message = {}
      for key, value in asdict(self).items():
          if value is not None:
              message[f'{key}'] = value
      return message
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
class MessageFactory(ABC):
  @staticmethod
  @abstractmethod
  def create_message(message_type: str, **kwargs) -> Any:
    raise NotImplementedError