import requests
import pandas as pd

def gettokenInfo(token_df, symbol, exch_seg = 'NSE', instrumenttype = 'OPTIDX', strike_price = '', pe_ce = 'CE' ):
    strike_price = strike_price * 100

    if exch_seg == 'NSE':
        eq_df = token_df[(token_df['exch_seg'] == 'NSE') & (token_df['symbol'].str.contains('EQ'))]
        return eq_df[eq_df['name'] == symbol]

    elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
        return token_df[(token_df['exch_seg'] == 'NFO') & (token_df['instrumenttype'] == instrumenttype) & (token_df['name'] == symbol)].sort_values(by=['expiry'])
    
    elif exch_seg == 'NFO' and ((instrumenttype == 'OPTSTK') or (instrumenttype == 'OPTIDX')):
        return token_df[(token_df['exch_seg'] == 'NFO') & (token_df['instrumenttype'] == instrumenttype) & (token_df['name'] == symbol) & (token_df['strike'] == strike_price) & (token_df['symbol'].str.endswith(pe_ce))].sort_values(by=['expiry'])

def get_token_api():
    # global token_df
    json_url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    try:
        response  = requests.get(json_url, verify=True)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        # print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


    if response.status_code == 200:
        json_data = response.json()
        token_df = pd.DataFrame.from_dict(json_data)
        token_df['expiry'] = pd.to_datetime(token_df['expiry'])
        token_df = token_df.astype({'strike':float})
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_rows', None)
        token_df.drop(columns=['expiry', 'strike', 'lotsize', 'tick_size'], inplace = True)
        token_df.reset_index(drop=True)
        # os.system('python example/get_token.py > company_token_list.txt')
        # print(token_df)
        token_df.to_csv('company_token_list.csv', index=False)
        # os.system('print(token_df) > company_token_list.txt')
    else: 
        print(f"Failed to fetch data. Status code: {response.status_code}")
    # token_df.to_csv(r'C:\Users\panch\Desktop\Prashant\smartapi-python' + 'angle_token.csv', header=True, index=False) #for save file into csv format
    # token_info = gettokenInfo(token_df, 'NFO', 'OPTIDX', 'NIFTY', 21400, 'PE')
    # print(token_info)

    # token_info = gettokenInfo(token_df, 'ITC')  #ITC=1660, IEX = 220, CDSL = 21174
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.width', None)
    # pd.set_option('display.max_rows', None)
    # print(token_info, "\n\n\n")
    # print(token_info['name'])
    # print(token_info['symbol'] )
    # print(token_info['token'])
    # print(token_info['lotsize'])

# get_token_api()
# place order
