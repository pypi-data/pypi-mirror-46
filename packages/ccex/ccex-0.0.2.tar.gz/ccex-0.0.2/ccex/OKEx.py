import websocket
import threading
import json
import sys
import os
import zlib
import hmac
import base64
import requests
from datetime import datetime, timedelta, timezone 
import pandas as pd

CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'
APPLICATION_JSON = 'application/json'
FMT_TIME = "%Y-%m-%dT%H:%M:%S.%fZ"

# signature
def signature(timestamp, method, request_path, body, secret_key):
    if str(body) == '{}' or str(body) == 'None':
        body = ''
    message = str(timestamp) + str.upper(method) + request_path + str(body)
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)


# set request header
def get_header(api_key, sign, timestamp, passphrase):
    header = dict()
    header[CONTENT_TYPE] = APPLICATION_JSON
    header[OK_ACCESS_KEY] = api_key
    header[OK_ACCESS_SIGN] = sign
    header[OK_ACCESS_TIMESTAMP] = str(timestamp)
    header[OK_ACCESS_PASSPHRASE] = passphrase
    return header


def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        url = url + str(key) + '=' + str(value) + '&'

    return url[0:-1]

def parse_message(msg):
    def inflate(data):
        decompress = zlib.decompressobj(-zlib.MAX_WBITS)
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated
    
    return json.loads(inflate(msg))

class OKEx():
    def __init__(self):
        self.url_ws = 'wss://real.okex.com:10442/ws/v3'
        self.url_rest = 'https://www.okex.me'
        self.req_depth = ''
        self.cb_depth = None   # call back function for depth message
        self.api_key = ''
        self.secret_key = ''
        self.passphrase = ''
    
    def set_key(self, filename):
        df = pd.read_csv(filename, header = None)
        d = dict(zip(df[0],df[1]))
        self.api_key = d['api_key']
        self.secret_key = d['secret_key']
        self.passphrase = d['passphrase']
    
    def subscribe_depth(self,args,cb):
        self.req_depth = {"op": "subscribe", "args": args}
        self.cb_depth = cb
        self.ws = websocket.WebSocketApp(self.url_ws, 
                                         on_open = self.on_open_depth,
                                         on_message = self.on_message_depth,
                                         on_error= self.on_error)
        
        wst = threading.Thread(target=lambda:self.ws.run_forever())
        wst.daemon = True
        wst.start()
        
    def on_error(self, msg):
        print(msg)

    def on_open_depth(self):
        print("OKEx: on_open_depth, subscribe depth ...", self.req_depth)
        self.ws.send(json.dumps(self.req_depth))
    
    def on_message_depth(self,msg): 
        self.cb_depth(msg)

    def get_time(self):
        return requests.get(self.url_rest + '/api/general/v3/time').json()
    
    def get_instruments(self):
        instruments = requests.get(self.url_rest + '/api/futures/v3/instruments').json()
        df = pd.DataFrame()
        for ins in instruments:
            df = df.append(ins, ignore_index=True)
        return df

    def get_trades(self,stype,symbol,lmt=1):
        trades = requests.get(self.url_rest + '/api/{}/v3/instruments/{}/trades?limit={}'.format(stype,symbol,lmt)).json()
        df = pd.DataFrame()
        for i in trades:
            df = df.append(i, ignore_index=True)
        df['price'] = df.price.astype(float)
        return df

    
    def get_response(self, request_path):
        ts = float(self.get_time()['epoch'])
        header = get_header(self.api_key, signature(ts, 'GET', request_path, '', self.secret_key), ts, self.passphrase)
        response = requests.get(self.url_rest + request_path, headers=header)
        return response.json()
    
    def get_k_data(self, symbol, granularity):
        request_path = '/api/spot/v3/instruments/{}/candles?granularity={}'.format(symbol, granularity)

        data = self.get_response(request_path)
        df = pd.DataFrame(data,columns=['time','open','high','low','close','volume'])
        
        df['time'] = [datetime.strptime(t,FMT_TIME).replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8))).strftime(FMT_TIME)
                 for t in df.time]
        
        for c in df.columns[1:]:
            df[c] = df[c].astype(float)

        return df

        

    
if __name__ == '__main__':
    ex = OKEx()
    ex.set_key('key.csv')
#    ex.subscribe_depth(["spot/depth5:ETH-USDT","futures/depth5:BTC-USD-190510"],lambda x: print(parse_message(x)))
#    while(True):
#        continue