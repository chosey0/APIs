import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from layout.KoreaInvestments.messages import OverseasMinuteCandle
from core.agent.korea_investments import KISAgent

def main():
    KISAgent.read_token()
    message = OverseasMinuteCandle.create_message("TSLA")
    data = KISAgent.get(**message)
    print(OverseasMinuteCandle.handler(data))
    
if __name__ == "__main__":
    main()