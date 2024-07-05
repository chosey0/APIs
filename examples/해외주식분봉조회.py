import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from layout.KoreaInvestments.messages import OverseasMinuteCandle
from core.agent.korea_investments import KISAgent

from pprint import pprint

def main():
    message = OverseasMinuteCandle.create_message("TSLA")
    pprint(KISAgent.get(**message)["output2"])
    
if __name__ == "__main__":
    main()