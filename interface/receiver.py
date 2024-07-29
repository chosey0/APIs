import asyncio

class Receiver():
  def __init__(self, queue: asyncio.Queue):
    self.queue = queue
  
  async def receive_loop(self, session):
    while True:
        message = await session.recv()
        await self.queue.put(message)
        
      
class Processor():
    def __init__(self, queue: asyncio.Queue):
      self.queue = queue
    
    async def processing_loop(self, DQM):
      while True:
          if not self.queue.empty():
            message = await self.queue.get()
            statusType, tr_id, cnt, recvstr = message.split("|")
            
            if statusType == "0":
                data = recvstr.split("^")
                
                if not hasattr(DQM, f"{data[0]}"):
                    DQM.add_queue(f"{data[0]}", asyncio.Queue())
                    
                DQM.get(f"{data[0]}").put([cnt, data])
                
            elif statusType == "1":
                continue
            else:
                continue
          else:
            asyncio.sleep(0.01)