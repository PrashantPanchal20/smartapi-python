# # from optionchain_stream import OptionChain
# # OptionStream = OptionChain("option_symbol", "option_expiry_date in yyyy-mm-dd format", "api_key",
# #                     "api_secret=None", "request_token=None", "access_token=None", underlying=False)

# # # You can directly pass access_token from previous active session 
# # OptionStream = OptionChain("ONGC", "2021-02-25", "your_api_key", access_token="XXXXXX")

# # # Generate new session by passing api_secret and request_token
# # OptionStream = OptionChain("ONGC", "2021-02-25", "your_api_key", api_secret="XXXXX",
# #                     request_token="XXXXXX")

# # # You can fetch underlying stock tick as well in option chain, by sending optional param `underlying=True`
# # OptionStream = OptionChain("ONGC", "2021-02-25", "your_api_key", access_token="XXXXXX", underlying=True) 
# # OptionStream = OptionChain("ONGC", "2021-02-25", "your_api_key", api_secret="XXXXX",request_token="XXXXXX", underlying=True)


# # # Sync master instrument data to DB(redis)     
# # # This sync is required only once daily at initial run             
# # OptionStream.sync_instruments()

# # # Stream option chain data in real-time
# # StreamData = OptionStream.create_option_chain()
# # for data in StreamData:
# #     print(data)

import sys
sys.path.append( '/home/ppanchal/.local/lib/python2.7/site-packages' )


# import requests
# import json
# import pandas as pd
# # from pandas.io.json.json_normalize import json_normalize
# from pandas.io.json import json_normalize

# urlheader = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
#     "authority": "www.nseindia.com",
#     "scheme":"https"
# }

# expiry_dt = '28-June-2023'
# url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
# data = requests.get(url, headers=urlheader).content
# data2 = data.decode('utf-8')
# df = json.loads(data2)
# json_ce = eval("[data['CE'] for data in df['records']['data'] if 'CE' in data and data['expiryDate'] == '" + expiry_dt + "']")
# df_ce = json_normalize(json_ce)
# print('*** NIFTY Call Options Data with Expiry Date: '+ expiry_dt + ' *** \n', df_ce)
# json_pe = eval("[data['CE'] for data in df['records']['data'] if 'PE' in data and data['expiryDate'] == '" + expiry_dt + "']")
# df_pe = json_normalize(json_pe)
# print('*** NIFTY Put Options Data with Expiry Date: '+ expiry_dt + ' *** \n', df_pe)





import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

# data = pd.read_csv('../Data/RELIANCE.csv', parse_dates=['Date'], index_col='Date')
# print(data)

def GoldenCrossverSignal(name):
    path = f'/home/ppanchal/Prashant_Panchal/market/{name}.csv'
# /home/ppanchal/Prashant_Panchal/market/RELIANCE.csv
    data = pd.read_csv(path, parse_dates=['Date'], index_col='Date')
    print(data)
    print('========================================',type(data))
    data['20_SMA'] = data.Close.rolling(window=20, min_periods=1).mean()
    data['50_SMA'] = data.Close.rolling(window=50, min_periods=1).mean()
    data['Signal'] = 0
    data['Signal'] = np.where(data['20_SMA'] > data['50_SMA'], 1, 0)
    data['Position'] = data.Signal.diff()
    # plt.figure(figsize = (20,10))
    # # plot close price, short-term and long-term moving averages 
    # data.iloc[-data_point:]['Close'].plot(color = 'k', label= 'Close Price') 
    # data.iloc[-data_point:]['20_SMA'].plot(color = 'b',label = '20-day SMA') 
    # data.iloc[-data_point:]['50_SMA'].plot(color = 'g', label = '50-day SMA')
    # # plot ‘buy’ signals
    # plt.plot(data.iloc[-data_point:][data.iloc[-data_point:]['Position'] == 1].index, 
    #          data.iloc[-data_point:]['20_SMA'][data.iloc[-data_point:]['Position'] == 1], 
    #          '^', markersize = 15, color = 'g', label = 'buy')
    # # plot ‘sell’ signals
    # plt.plot(data.iloc[-data_point:][data.iloc[-data_point:]['Position'] == -1].index, 
    #          data.iloc[-data_point:]['20_SMA'][data.iloc[-data_point:]['Position'] == -1], 
    #          'v', markersize = 15, color = 'r', label = 'sell')
    # plt.ylabel('Price in Rupees', fontsize = 15 )
    # plt.xlabel('Date', fontsize = 15 )
    # plt.title(name, fontsize = 20)
    # plt.legend()
    # plt.grid()
    # plt.show()
    # df_pos = data.iloc[-data_point:][(data.iloc[-data_point:]['Position'] == 1) | (data['Position'] == -1)].copy()
    df_pos = data[data(['Position'] == 1) | data(['Position'] == -1)].copy()
    df_pos['Position'] = df_pos['Position'].apply(lambda x: 'Buy' if x == 1 else 'Sell')
    # print(tabulate(df_pos[['Close', 'Position']], headers = 'keys', tablefmt = 'psql'))
    return df_pos

GoldenCrossverSignal('RELIANCE')
