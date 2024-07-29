import asyncio
import json
import websockets
from datetime import datetime


URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"
msg = {
  "method": "SUBSCRIBE",
  "params": [
    "btcusdt@trade",
  ],
  "id": 1
}

def handle_trades(json_message):
    date_time = datetime.fromtimestamp(json_message['E']/1000).strftime('%Y-%m-%d %H:%M:%S')
    print("Symbol: "+json_message['s'])
    print("Price: "+json_message['p'])
    print("Quantity: "+json_message['q'])
    print("TIMESTAMP: " + str(date_time))
    print("-----------------------")

async def main():

    async with websockets.connect(URL) as websocket:
        await websocket.send(json.dumps(msg))
        response = await websocket.recv()
        print(response)
        
        while True:
            response = json.loads(await websocket.recv())
            if response.get("e") == "trade":
                handle_trades(response)

if __name__ == "__main__":
    asyncio.run(main())