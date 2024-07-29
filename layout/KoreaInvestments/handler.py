import toolz.itertoolz as tz
import threading
import queue
import time
import asyncio

def overseas_websockets_processor(data_queue: queue.Queue, handler, recvstr: str):
  """_summary_

  Args:
      recvstr (str): _description_
      data: symbol, ndiv, local_bdate, local_date, local_time, kr_date, kr_time, open, high, low, close, sign, diff, rate, bid, ask, bid_v, ask_v, trade_v, trade_amount, bid_trade_v, ask_trade_v, trade_power, market_type
  Returns:
      _type_: _description_
  """
  
  status_code, tr_id, cnt, datastr = recvstr.split("|")
  
  while True:
    if data_queue.empty():
      time.sleep(0.01)
      data_queue.task_done()
      
    else:
      data = data_queue.get()
            
      handler(data)
      data_queue.task_done()
    

  
def handling(data):
  keys = ['symbol', 'ndiv', 'local_bdate', 'local_date', 'local_time', 'kr_date', 'kr_time', 'open', 'high', 'low', 'close', 'sign', 'diff', 'rate', 'bid', 'ask', 'bid_v', 'ask_v', 'trade_v', 'trade_amount', 'bid_trade_v', 'ask_trade_v', 'trade_power', 'market_type']

  parsed_data = dict(zip(keys, data))
  
  return {key: parsed_data[key] for key in ['symbol', 'local_date', 'local_time', 'open', 'high', 'low', 'close', 'trade_v', 'trade_amount']} 
  
  data = datastr.split("^")
  
  if int(cnt) > 1:
    return [handling(d) for d in data]
  
  else:
    return handling(data)