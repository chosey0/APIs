import sys
import os
import pandas as pd
import asyncio
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from layout.KoreaInvestments.messages import Subscribe
from core.agent.korea_investments import KISAgent, KISWebSocketAgent
from layout.KoreaInvestments.tr_code import TRCode, TRKey

async def main():
  agent = KISWebSocketAgent(tr_id=TRCode.overseas_transaction)
  agent.start()
  
  df = pd.read_csv("data/stock_info/nas_code.csv", header="infer")[["realtime symbol", "Korea name", "Symbol"]]
  
  message = Subscribe.create_message(
    approval_key=KISAgent.get_approval_key(), 
    tr_id=TRCode.overseas_transaction, 
    stock_code=f"{TRKey.USA_DAY}{TRKey.USA_DAY_NASDAQ}{df[df['Korea name'] == '엔비디아']['Symbol'].values[0]}"
  )

  await agent.send(message)
  agent.join()
  
    
if __name__ == "__main__":
    asyncio.run(main())