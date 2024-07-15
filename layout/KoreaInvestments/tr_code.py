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
  """ https://apiportal.koreainvestment.com/apiservice/apiservice-oversea-stock-real2#L_52290e93-e94c-4d2a-9ce3-c304681d3807
      <미국 야간거래/아시아 주간거래>
      D+시장구분(3자리)+종목코드
      예) DNASAAPL : D+NAS(나스닥)+AAPL(애플)
      [시장구분]
      NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 ,
      TSE : 도쿄, HKS : 홍콩,
      SHS : 상해, SZS : 심천
      HSX : 호치민, HNX : 하노이

      <미국 주간거래>
      R+시장구분(3자리)+종목코드
      예) RBAQAAPL : R+BAQ(나스닥)+AAPL(애플)
      [시장구분]
      BAY : 뉴욕(주간), BAQ : 나스닥(주간). BAA : 아멕스(주간)
  """
  
  USA_DAY: str = "R"
  USA_DAY_NASDAQ: str = "BAQ"
  USA_DAY_NEWYORK: str = "BAY"
  USA_DAY_AMEX: str = "BAA"
  
  USA_LOCAL: str = "D"
  NASDAQ: str = "NAS"
  NEWYORK: str = "NYS"
  AMEX: str = "AMS"
  
  