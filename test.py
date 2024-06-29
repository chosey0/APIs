import os    
import ccxt.pro as ccxtpro
import asyncio
import pprint

async def main():
    exchange = ccxtpro.binance(config={
        'apiKey': os.getenv("BINANCE_RAPP"),
        'secret': os.getenv("BINANCE_RSEC"),
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future'
        }
    })

    while True:
        ticker = await exchange.watch_trades(symbol="BTC/USDT")
        pprint.pprint(ticker)

asyncio.run(main())