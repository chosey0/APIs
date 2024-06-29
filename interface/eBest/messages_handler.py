import pandas as pd
import numpy as np

def chart_data_handler(data):
    # Create DataFrame and parse datetime
    df = pd.DataFrame(data)
    df["Time"] = pd.to_datetime(df["date"] + df["time"], format="%Y%m%d%H%M%S")
    
    # Select and rename columns
    df = df[["Time", "open", "high", "low", "close"]].rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close"})
    
    # Calculate moving averages
    df["ma20"] = df["Close"].rolling(window=20).mean()
    df["ma120"] = df["Close"].rolling(window=120).mean()
    
    # Drop rows with NaN values
    df.dropna(inplace=True)
    
    # Add additional columns with NaN values
    for col in ["low_point", "high_point", "low_prob", "high_prob", "none_prob"]:
        df[col] = np.nan
    
    # Set index as datetime in milliseconds
    df.set_index(df["Time"].astype(np.int64) // 10**6, inplace=True)
    
    # Convert specific columns to float64
    df[["Open", "Close", "High", "Low"]] = df[["Open", "Close", "High", "Low"]].astype(np.float64)
    
    # Return the final DataFrame
    return df[["Time", "Open", "Close", "High", "Low", "ma20", "ma120", "low_point", "high_point", "low_prob", "high_prob", "none_prob"]]