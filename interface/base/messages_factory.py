from typing import Dict, Any, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Union

import json
import os


@dataclass
class BaseMessage:
    attributes: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        for key, value in self.attributes.items():
            setattr(self, key, value)
    
    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls(attributes=kwargs)
    
    def to_dict(self):
        message = {}
        for key, value in self.attributes.items():
            if value is not None:
                message[f'{key}'] = value
        return message
    
    def to_tuple(self):
        return tuple(self.attributes.values())
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def add_attribute(self, key: str, value: Any):
        self.attributes[key] = value
        
        return self
    
class MessageStrategy:
    @staticmethod
    @abstractmethod
    def create_message(**kwargs) -> Union[BaseMessage, NotImplementedError]:
        return NotImplementedError

