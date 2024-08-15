import os
import pandas as pd
from binance.client import Client

def fetch_btc_data():
    apikey = os.getenv('APIKEY')
    secret = os.getenv('SECRET')
    client = Client(apikey, secret)
    historical = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1DAY, '1 Jan 2011')
    hist_df = pd.DataFrame(historical)
    hist_df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
                        'Quote Asset Volume', 'Number of Trades', 'TB Base Volume',
                         'TB Quote Volume', 'Ignore']
    hist_df['Open Time'] = pd.to_datetime(hist_df['Open Time']/1000, unit='s')
    hist_df['Close Time'] = pd.to_datetime(hist_df['Close Time']/1000, unit='s')
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume',
                        'Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']
    hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric, axis=1)
    return hist_df

if __name__ == "__main__":
    df = fetch_btc_data()
    df.to_csv('btc_data.csv', index=False)
    print("Data fetched and saved to btc_data.csv")
