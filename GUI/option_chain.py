import sys
sys.path.append( '/home/ppanchal/.local/lib/python2.7/site-packages' )
sys.path.append('/home/ppanchal/Prashant_Panchal/GUI/site-packages/traitlets/')

import json
import requests
import json
import math
import argparse
import pandas as pd
# import numpy as np
# import chart_all as chart

# parser = argparse.ArgumentParser(description='Parse and sort defines and plusargs from a Verilog file.')
# parser.add_argument('-o', '--index_name', help='TO get index name form terminal', default='')
# args = parser.parse_args()

def data_fetch(index_name, num_strike):

    import requests
    import pandas as pd
    import time
    global df

    def strRed(skk):         return "\033[91m {}\033[00m".format(skk)
    def strGreen(skk):       return "\033[92m {}\033[00m".format(skk)
    def strYellow(skk):      return "\033[93m {}\033[00m".format(skk)
    def strLightPurple(skk): return "\033[94m {}\033[00m".format(skk)
    def strPurple(skk):      return "\033[95m {}\033[00m".format(skk)
    def strCyan(skk):        return "\033[96m {}\033[00m".format(skk)
    def strLightGray(skk):   return "\033[97m {}\033[00m".format(skk)
    def strBlack(skk):       return "\033[98m {}\033[00m".format(skk)
    def strBold(skk):        return "\033[1m {}\033[0m".format(skk)

    def set_cookie():
        request = sess.get(url_oc, headers=headers, timeout=5)
        cookies = dict(request.cookies)

    def get_data(url):
        set_cookie()
        response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
        if(response.status_code==401):
            set_cookie()
            response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
        if(response.status_code==200):
            return response.text
        return ""
    
    def highest_oi_CE_PE(num_strike,step,nearest):
        global max_oi_strike_CE, max_oi_strike_PE, max_oi_CE, max_oi_PE, max_vol_CE, max_vol_PE, Change_OI_CE, Change_OI_PE 
        global max_vol_strike_CE, max_vol_strike_PE, Change_OI_strike_PE, Change_OI_strike_CE

        num = int(num_strike)
        strike = nearest - (step*num)
        start_strike = nearest - (step*num)
        max_oi_CE = 0
        max_oi_PE = 0
        max_oi_strike_CE = 0
        max_oi_strike_PE = 0
        max_vol_CE = 0
        max_vol_strike_CE = 0
        max_vol_PE = 0
        max_vol_strike_PE = 0
        Change_OI_CE = 0
        Change_OI_strike_CE = 0
        Change_OI_PE = 0
        Change_OI_strike_PE = 0

        for item in data['records']['data']:
            if item["expiryDate"] == currExpiryDate:
                if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                    if item["CE"]["openInterest"] > max_oi_CE:
                        max_oi_strike_CE = item["strikePrice"]
                        max_oi_CE = item["CE"]["openInterest"]

                    if item["PE"]["openInterest"] > max_oi_PE:
                        max_oi_PE = item["PE"]["openInterest"]
                        max_oi_strike_PE = item["strikePrice"]

                    if item["CE"]["totalTradedVolume"] > max_vol_CE:
                        max_vol_strike_CE = item["strikePrice"]
                        max_vol_CE = item["CE"]["totalTradedVolume"]

                    if item["PE"]["totalTradedVolume"] > max_vol_PE:
                        max_vol_PE = item["PE"]["totalTradedVolume"]
                        max_vol_strike_PE = item["strikePrice"]

                    if item["CE"]["changeinOpenInterest"] > Change_OI_CE:
                        Change_OI_strike_CE = item["strikePrice"]
                        Change_OI_CE = item["CE"]["changeinOpenInterest"]

                    if item["PE"]["changeinOpenInterest"] > Change_OI_PE:
                        Change_OI_PE = item["PE"]["changeinOpenInterest"]
                        Change_OI_strike_PE = item["strikePrice"]

                    # PCR()
                    strike = strike + step

    def data_arange():
        global data_frame_OP

        zipped = list(zip(date, call_OI, call_change_OI, call_changePresent_OI,call_IV, call_volume, call_LTP, strike_price,put_LTP, put_volume, put_IV, put_changePresent_OI, put_change_OI, put_OI))
        data_frame_OP = pd.DataFrame(zipped, columns=['Date','Call OI','Change OI', '% Change OI','Call IV', 'Volume','Call LTP', 'STRIKE','Put LTP','Volume','Put IV','% Change OI','Change OI','Put OI'])
        # print(data_frame_OP)
        # plot_OI(data_frame_OP)

    def PCR():
        global total_pcr, currentday_pcr
        # print(call_OI, put_OI)    
        put_sum = sum(list(map(int,[s.strip() for s in  put_OI])))
        call_sum = sum(list(map(int,[s.strip() for s in  call_OI])))      
        total_pcr = "%.4f" % (put_sum/call_sum)

        put_change_sum = sum(list(map(int,[s.strip() for s in  put_change_OI])))
        call_change_sum = sum(list(map(int,[s.strip() for s in  call_change_OI])))      
        currentday_pcr = "%.4f" % (put_change_sum/call_change_sum)      
  
    def oi_data(num_strike,step,nearest,url):
        global data, response_text, currExpiryDate
        global date, call_OI, call_change_OI, call_changePresent_OI,call_IV, call_volume, call_LTP
        global strike_price,put_LTP, put_volume,put_IV, put_changePresent_OI, put_change_OI, put_OI
        date = [] 
        call_OI = []
        call_change_OI = []
        call_changePresent_OI = []
        call_IV = []
        call_volume = []
        call_LTP = []
        strike_price = []
        put_LTP = []
        put_volume = []
        put_IV = []
        put_changePresent_OI = []
        put_change_OI = []
        put_OI = []  
        num = int(num_strike)
        strike = nearest - (step*num)
        start_strike = nearest - (step*num)
        response_text = get_data(url)
        data = json.loads(response_text)
        currExpiryDate = data["records"]["expiryDates"][0]
        for item in data['records']['data']:
            if item["expiryDate"] == currExpiryDate:
                if (item["strikePrice"] == strike and item["strikePrice"] < start_strike + (step*num*2)):
                    date.append(data["records"]["expiryDates"][0])
                    # call_OI.append(strBold(str(item["CE"]["openInterest"]).rjust(6," ")))
                    call_OI.append(str(item["CE"]["openInterest"]).rjust(6," "))
                    call_change_OI.append(str(item["CE"]["changeinOpenInterest"]).rjust(6," "))
                    call_changePresent_OI.append(("%.2f" % item["CE"]["pchangeinOpenInterest"]).rjust(6," "))
                    call_IV.append(("%.2f" % item["CE"]["impliedVolatility"]).rjust(6," "))
                    call_volume.append(str(item["CE"]["totalTradedVolume"]).rjust(6," "))
                    call_LTP.append((item["CE"]["lastPrice"]))
                    strike_price.append(item["strikePrice"])
                    put_LTP.append((item["PE"]["lastPrice"]))
                    put_volume.append(str(item["PE"]["totalTradedVolume"]).rjust(6," "))
                    put_IV.append(("%.2f" % item["PE"]["impliedVolatility"]).rjust(6," "))
                    put_changePresent_OI.append(("%.2f" % item["PE"]["pchangeinOpenInterest"]).rjust(6," "))
                    put_change_OI.append(str(item["PE"]["changeinOpenInterest"]).rjust(6," "))
                    put_OI.append(str(item["PE"]["openInterest"]).rjust(6," "))
                    strike = strike + step
        data_arange()   #4
        PCR()


    # Method to get nearest strikes
    def round_nearest(x,num=50): 
        return int(math.ceil(float(x)/num)*num)

    def nearest_strike_bnf(x): 
        return round_nearest(x,100)

    def nearest_strike_nf(x): 
        return round_nearest(x,50)

    def nearest_strike_midf(x): 
        return round_nearest(x,25)
    
    def header(index="",ul=0,nearest=0):
        global header_values

        header_values = index.ljust(5," ") + " => "+ " Last Price: " + str(ul) + "   Nearest Strike: " + str(nearest)

    def set_header(index_name):
        
        global ul
        global nearest
        response_text = get_data(url_indices)
        data = json.loads(response_text)
        if index_name == "NIFTY":
            for index in data["data"]:
                if index["index"]=="NIFTY 50":
                    ul = index["last"]
                    nearest=nearest_strike_nf(ul)
                    header(index_name,ul,nearest)  #2

        if index_name == "BANKNIFTY":
            for index in data["data"]:
                if index["index"]=="NIFTY BANK":
                    ul = index["last"]
                    nearest=nearest_strike_bnf(ul)
                    header(index_name,ul,nearest)  #2

        if index_name == "FINNIFTY":
            for index in data["data"]:
                if index["index"]=="NIFTY FINANCIAL SERVICES": #https://www.nseindia.com/api/allIndices
                    ul = index["last"]
                    nearest=nearest_strike_nf(ul)
                    header(index_name,ul,nearest)  #2

        if index_name == "MIDCPNIFTY":
            for index in data["data"]:
                if index["index"]=="NIFTY MIDCAP LIQUID 15":  #https://www.nseindia.com/api/allIndices
                    ul = index["last"]
                    nearest=nearest_strike_midf(ul)
                    header(index_name,ul,nearest)  #2

    try:
        url_oc      = "https://www.nseindia.com/option-chain"
        url_indices = "https://www.nseindia.com/api/allIndices"
        url = f'https://www.nseindia.com/api/option-chain-indices?symbol={index_name}'
        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language":"en-US,en;q=0.9",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36" }

        sess = requests.Session()
        cookies = dict()
        set_header(index_name)   #1
        if index_name == "NIFTY":
            oi_data(num_strike,50,nearest,url)   #3
            highest_oi_CE_PE(num_strike,50,nearest)  #5
        if index_name == "BANKNIFTY":
            oi_data(num_strike,100,nearest,url)   #3
            highest_oi_CE_PE(num_strike,100,nearest)  #5
        if index_name == "FINNIFTY":
            oi_data(num_strike,50,nearest,url)   #3
            highest_oi_CE_PE(num_strike,50,nearest)  #5
        if index_name == "MIDCPNIFTY":
            oi_data(num_strike,25,nearest,url)   #3
            highest_oi_CE_PE(num_strike,25,nearest)  #5

    except Exception as e :
        print(e)

# data_fetch(args.index_name)
