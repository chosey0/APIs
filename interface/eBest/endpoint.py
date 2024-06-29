from dataclasses import dataclass

@dataclass
class Endpoint:
    base_url: str = "https://openapi.ls-sec.co.kr:8080"
    get_token: str = 'oauth2/token'
    revoke_token: str = 'oauth2/revoke'
    get_minute_candle: str = "stock/chart"
    tick_chart: str = "stock/chart"