import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from layout.KoreaInvestments.messages import OverseasDayCandle
from core.agent.korea_investments import KISAgent

def main():
    message = OverseasDayCandle.create_message("TSLA")
    data = KISAgent.get(**message)
    print(OverseasDayCandle.handler(data))
    
if __name__ == "__main__":
    main()