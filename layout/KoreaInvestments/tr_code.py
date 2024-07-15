from dataclasses import dataclass

@dataclass
class TRCode:
  transaction: str = "H0STCNT0" # 체결가
  transaction_notify: str = "H0STCNI0" # 체결 통보
  order_book: str = "H0STASP0" # 호가
  
  overseas_day_candle: str = "HHDFS76240000" # 일봉
  overseas_minute_candle: str = "HHDFS76950200" # 분봉
  
  overseas_transaction: str = "HDFSCNT0" # 실시간 지연 체결가
  overseas_transaction_notify: str = "H0GSCNI0" # 실시간 체결 통보
  usa_order_book: str = "HDFSASP0" # 실시간 지연 호가
  
  subscribe: str = "1"
  unsubscribe: str = "2"
  
@dataclass
class TRKey:
  tr_key: str