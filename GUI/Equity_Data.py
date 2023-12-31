# recure =========>>>>>>>>>>>>   pip install yfinance, pip install yfinance --upgrade --no-cache-dir
# https://pypi.org/project/yfinance/
# pip install yfinance==0.1.57
# pip install yfinance==0.1.68
# https://finance.yahoo.com/quote/RELIANCE.NS/history?p=RELIANCE.NS

import sys
sys.path.append( '/home/ppanchal/.local/lib/python2.7/site-packages' )

import yfinance as yf
import pandas as pd
import autocompletecombobox as autocomp
from tkinter.filedialog import asksaveasfilename
# Example=============================ony one compny data ===========================
# data = yf.download('TCS.NS')
# data.to_csv('TCS.csv')
# print(data)

# ======================================for multiple compny data ===========================
# ==========>> https://www.nseindia.com/market-data/securities-available-for-trading  ==>> It will provide a list of company

def quity_data():
    global symbol, equity_details

    url = 'https://archives.nseindia.com/content/equities/EQUITY_L.csv'
    equity_details = pd.read_csv(url) # All Details for NSE stocks : Symbol is the required field
    # print(equity_details)
    symbol = []
    for item in equity_details.SYMBOL:
        symbol.append(item)

def check_data(name):
    global data
    try:
        data = yf.download(f'{name}.NS')
        # data.to_csv(f'./Data/{name}.csv') # Data will be stored in data folder
    except Exception as e:
        print(f'{name} ===> {e}')

# def download_data(name):
    
#     try:
#         data = yf.download(f'{name}.NS')
#         print(data)
#         # data.to_csv(f'./Data/{name}.csv') # Data will be stored in data folder
#     except Exception as e:
#         print(f'{name} ===> {e}')

def export_data(name):
    global op_field, data

    try:
        data = yf.download(f'{name}.NS')
            # print(data)
            # data.to_csv(f'./Data/{name}.csv') # Data will be stored in data folder

        files0 = [('Report', '*.csv'),('All Files', '*.*')]
        file = asksaveasfilename(title="Save As", filetypes = files0, defaultextension='*.csv')

        if file :
            print(file)
            oFile = open('file', "w")
            print(oFile)
            oFile.writelines(str(data))
            oFile.close()

    except Exception as e:
        print(f'{name} ===> {e}')
