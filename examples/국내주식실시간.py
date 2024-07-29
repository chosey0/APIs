import sys
import os
import pandas as pd
import asyncio
import threading
import time


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from layout.KoreaInvestments.messages import Subscribe
from core.agent.korea_investments import KISAgent, KISWebSocketAgent
from layout.KoreaInvestments.tr_code import TRCode, TRKey

async def main():
  try:
    message_queue = asyncio.Queue()
    agent = KISWebSocketAgent(tr_id=TRCode.transaction)
    agent.callback = message_queue.put
    agent.start()
    
    df = pd.concat([pd.read_csv("data/stock_info/kosdaq_code.csv", header="infer")[["단축코드", "한글종목명"]], 
                    pd.read_csv("data/stock_info/kospi_code.csv", header="infer")[["단축코드", "한글종목명"]]], axis=0, ignore_index=True)

    message = Subscribe.create_message(
      approval_key=KISAgent.get_approval_key(), 
      tr_id=TRCode.transaction, 
      stock_code=f"{df[df['한글종목명'] == '와이씨']['단축코드'].values[0]}"
    )

    await agent.send(message)
    
    # agent.join()
    while True:
      print(message_queue.qsize())
      dt, data = await message_queue.get()
      print(dt, data)
      time.sleep(1)
      continue
    
  except KeyboardInterrupt:
    print("Stopping...")
    agent.stop()
    
    
      
    
if __name__ == "__main__":
    asyncio.run(main())