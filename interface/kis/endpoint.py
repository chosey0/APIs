from dataclasses import dataclass
from urllib.parse import urljoin

@dataclass
class Endpoint:
    base_url: str = "https://openapi.koreainvestment.com:9443"
    ws_base_url: str = "ws://ops.koreainvestment.com:21000"
    get_token: str = 'oauth2/tokenP'
    revoke_token: str = 'oauth2/revokeP'
    approval_key: str = "oauth2/Approval"
    
    transaction: str = "tryitout/H0STCNT0"
    transaction_notify: str = "tryitout/H0STCNI0"
    order_book: str = "tryitout/H0STASP0"
    
    overseas_transaction: str = "tryitout/HDFSCNT0"
    overseas_transaction_notify: str = "tryitout/H0GSCNI0"
    usa_order_book: str = "tryitout/HDFSASP0"
