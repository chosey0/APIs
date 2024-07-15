def overseas_websockets(datastr: str):
  status_code, tr_id, cnt, raw_datastr = datastr.split("|")
  
  symbol, ndiv, local_bdate, local_date, local_time, kr_date, kr_time, open, high, low, close, sign, diff, rate, bid, ask, bid_v, ask_v, trade_v, trade_amount, bid_trade_v, ask_trade_v, trade_power, market_type = raw_datastr.split("^")
  
  
  