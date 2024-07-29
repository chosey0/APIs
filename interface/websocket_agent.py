from abc import ABC, abstractmethod


import websockets
from websockets import WebSocketClientProtocol

import asyncio
from typing import Union, Callable
import threading

class WebsocketAgent(threading.Thread):
  def __init__(self):
    super().__init__()
    self.setDaemon(True)
    self.name = "WebsocketAgent"
    self.url = "wss://echo.websocket.org"
    
    self.callback = None
    
    self.loop = asyncio.new_event_loop()
    
  async def connect(self):
    self.session = await websockets.connect(self.url, ping_interval=30)
    
  async def send(self, message):
    print(message)
    await self.session.send(message)

  async def receive(self):
      return await self.session.recv()

  async def close(self):
      await self.session.close()
      
  @abstractmethod
  async def receive_loop(self, callback: Callable):
    await self.connect()
    
    try:
        while True:
            message = await self.session.recv()
            callback(message)
    except websockets.ConnectionClosed:
        print("Connection closed")
        
    finally:
        await self.close()

  async def add_processor(self, tr_id: str, callback: Callable):
      self.processor[tr_id] = callback
      
  def run(self):
    loop = asyncio.new_event_loop()  # Create a new event loop for this thread
    asyncio.set_event_loop(loop)  # Set the new event loop as the current event loop
    loop.run_until_complete(self.receive_loop(self.callback))
    
  def stop(self):
      self.loop.call_soon_threadsafe(self.loop.stop)
      