from dataclasses import dataclass

@dataclass
class TRCode:
  transaction: str = "H0STCNT0"
  transaction_notify: str = "H0STCNI0"
  order_book: str = "H0STASP0"
  
  overseas_day_candle: str = "HHDFS76240000"
  overseas_minute_candle: str = "HHDFS76950200"
  
  overseas_transaction: str = "HDFSCNT0"
  overseas_transaction_notify: str = "H0GSCNI0"
  usa_order_book: str = "HDFSASP0"
  
  subscribe: str = "1"
  unsubscribe: str = "2"
  
@dataclass
class TRKey:
  tr_key: str