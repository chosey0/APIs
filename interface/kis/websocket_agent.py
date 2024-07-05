import websockets
from websockets import WebSocketClientProtocol
from interface.base.websocket_agent import WebsocketAgent

import asyncio
import json

from typing import Callable
from datetime import datetime, timezone



import logging

logger = logging.getLogger(__name__)

class KIS_WebsocketAgent(WebsocketAgent):
  def __init__(self):
    super().__init__()
    self.url = "ws://ops.koreainvestment.com:21000"

  async def receive_loop(self, callback: Callable):
    await self.connect()
    
    try:
        while True:
          data = await self.session.recv()
          recv_time = datetime.now(tz=timezone.utc).timestamp()
          
          if data[0] == '0':
              await callback([recv_time, data])
              
          elif data[0] == '1':
              continue
            
          else:
            jsonObject = json.loads(data)
            trid = jsonObject["header"]["tr_id"]
            
            if trid == "PINGPONG":
                logger.info(f"{data}")
                await self.session.pong(data)
            else:
              continue
    except websockets.ConnectionClosed:
        print("Connection closed")