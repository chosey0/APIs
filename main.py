from core.agent.ebest import eBestAgent
from core.agent.korea_investments import KISAgent, KISWebSocketAgent
from layout.KoreaInvestments.messages import Subscribe
from layout.KoreaInvestments.tr_code import TRCode

import logging
import asyncio
import json

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create handlers
info_handler = logging.FileHandler('log/info.log', encoding='utf-8')
info_handler.setLevel(logging.INFO)

error_handler = logging.FileHandler('log/error.log', encoding='utf-8')
error_handler.setLevel(logging.ERROR)

# Create formatters and add them to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(error_handler)

# Also add stream handler to see logs in console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

import pandas as pd

def main():
    logger = logging.getLogger(__name__)
    logger.info("Starting the main script")
    df = pd.read_csv("data/stock_info/nas_code.csv", header="infer")[["realtime symbol", "Korea name"]]
    msg = Subscribe.create_message(approval_key=KISAgent.get_approval_key(), tr_id=TRCode.overseas_transaction, stock_code=df[df["Korea name"] == "엔비디아"]["realtime symbol"].values[0])
    print(msg)
    # print(msg)
    # agent = KISWebSocketAgent()
    
    # agent.start()
    # agent.join()
    
if __name__ == "__main__":
    main()