import websocket
import threading
import json
import sys
import os
import zlib

class OKEx():
    def __init__(self):
        self.url_ws = "wss://real.okex.com:10442/ws/v3"
        self.req_depth = ''
        self.cb_depth = None   # call back function for depth message
        
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


def parse_message(msg):
    def inflate(data):
        decompress = zlib.decompressobj(-zlib.MAX_WBITS)
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated
    
    return json.loads(inflate(msg))
    
if __name__ == '__main__':
    ex = OKEx()
    ex.subscribe_depth(["spot/depth5:ETH-USDT","futures/depth5:BTC-USD-190510"],lambda x: print(parse_message(x)))
    while(True):
        continue