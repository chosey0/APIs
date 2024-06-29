from core.agent.ebest import eBestAgent
from core.agent.korea_investments import KISAgent
from interface.eBest.messages_handler import chart_data_handler

import logging

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

def main():
    logger = logging.getLogger(__name__)
    logger.info("Starting the main script")
    
    print(chart_data_handler(eBestAgent.get_chart_data("minute", shcode = "005930")["t8412OutBlock1"]))
if __name__ == "__main__":
    # from dotenv import load_dotenv
    # load_dotenv()
    
    main()