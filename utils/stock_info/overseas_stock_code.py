import os
import ssl
import zipfile
import urllib.request
from dataclasses import dataclass, field
from typing import List
import pandas as pd

@dataclass
class StockCodeDownloader:
    base_dir: str = os.path.join(os.getcwd(), "data", "stock_info")
    url_template: str = "https://new.real.download.dws.co.kr/common/master/{val}mst.cod.zip"
    columns: List[str] = field(default_factory=lambda: [
        'National code', 'Exchange id', 'Exchange code', 'Exchange name', 'Symbol', 'realtime symbol', 'Korea name', 
        'English name', 'Security type(1:Index,2:Stock,3:ETP(ETF),4:Warrant)', 'currency', 'float position', 
        'data type', 'base price', 'Bid order size', 'Ask order size', 'market start time(HHMM)', 'market end time(HHMM)', 
        'DR 여부(Y/N)', 'DR 국가코드', '업종분류코드', '지수구성종목 존재 여부(0:구성종목없음,1:구성종목있음)', 
        'Tick size Type', '구분코드(001:ETF,002:ETN,003:ETC,004:Others,005:VIX Underlying ETF,006:VIX Underlying ETN)',
        'Tick size type 상세'
    ])

    def download_and_extract(self, val: str):
        ssl._create_default_https_context = ssl._create_unverified_context
        
        url = self.url_template.format(val=val)
        zip_path = os.path.join(self.base_dir, f"{val}mst.cod.zip")
        
        urllib.request.urlretrieve(url, zip_path)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.base_dir)
            
        os.remove(zip_path)  # Clean up the downloaded zip file

    def get_dataframe(self, val: str) -> pd.DataFrame:
        self.download_and_extract(val)
        file_path = os.path.join(self.base_dir, f"{val}mst.cod")
        df = pd.read_table(file_path, sep='\t', encoding='cp949')
        df.columns = self.columns
        df.to_csv(f'{os.path.join(self.base_dir, val)}_code.csv', index=False, encoding="utf-8")  # Save as an Excel file
        return df

    def download_all_markets(self):
        markets = ['nas', 'nys', 'ams', 'shs', 'shi', 'szs', 'szi', 'tse', 'hks', 'hnx', 'hsx']
        combined_df = pd.DataFrame()
        for market in markets:
            temp_df = self.get_dataframe(market)
            combined_df = pd.concat([combined_df, temp_df], axis=0)
        combined_df.to_csv('overseas_stock_code(all).csv', index=False, encoding="utf-8")  # Save combined data as Excel file

    def download_specific_market(self, market_code: str):
        try:
            df = self.get_dataframe(market_code)
            print("Done")
        except Exception as e:
            print(f"Error downloading data for {market_code}: {e}")

def main():
    downloader = StockCodeDownloader()
    print(downloader.get_dataframe("nas")[["Korea name", "Symbol",  "realtime symbol"]])
    # cmd = "2"
    # cmd = input("1: Download all markets, 2: Download a specific market \n")

    # if cmd == '1':
    #     downloader.download_all_markets()
    # elif cmd == '2':
    #     market_code = "nas" # input("Enter the market code (e.g., nas, nys, ams, shs, shi, szs, szi, tse, hks, hnx, hsx): ")
    #     downloader.download_specific_market(market_code)

if __name__ == "__main__":
    main()