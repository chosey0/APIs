from typing import Dict, Any, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional
import json
from typing import ClassVar
@dataclass
class BaseMessage:
    attributes: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        for key, value in self.attributes.items():
            setattr(self, key, value)
    
    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls(attributes=kwargs)
    
    def to_dict(cls):
        message = {}
        for key, value in cls.attributes.items():
            if value is not None:
                message[f'{key}'] = value
        return message
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def add_attribute(self, key: str, value: Any):
        self.attributes[key] = value
        
        return self
    
class MessageStrategy(ABC):
    @staticmethod
    @abstractmethod
    def create_message(self, **kwargs) -> BaseMessage:
        pass
    
class MessageContext:
    @staticmethod
    def create_message(strategy: MessageStrategy, **kwargs) -> Dict:
        return strategy.create_message(**kwargs)
    
@dataclass(init=True)
class Header:
    attributes: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        for key, value in self.attributes.items():
            setattr(self, key, value)
    
    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls(attributes=kwargs)
    
    def to_dict(cls):
        headers = {}
        for key, value in cls.attributes.items():
            if value is not None:
                headers[f'{key}'] = value
        return headers
    
    @classmethod
    def to_json(cls):
        return json.dumps(cls.to_dict())

@dataclass(init=True)
class Body:
    attributes: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        for key, value in self.attributes.items():
            setattr(self, key, value)
    
    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls(attributes=kwargs)
    
    
    def to_dict(cls):
        body = {}
        for key, value in cls.attributes.items():
            if value is not None:
                body[f'{key}'] = value
        return body

    @classmethod
    def to_json(cls):
        return json.dumps(cls.to_dict())

