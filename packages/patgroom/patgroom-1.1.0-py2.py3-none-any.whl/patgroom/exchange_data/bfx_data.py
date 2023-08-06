# -*- coding: utf-8 -*-
"""
Description: 
Author     : Groom
Time       : 2018/10/9
File       : bfx_data.py
Version    : V0.1
"""
import pandas as pd

pd.set_option('expand_frame_repr', False)

def get_candles(symbol, TimeFrame, start='', end='', Section='hist', limit=1000, dataframe=False):
    if Section == 'hist':
        ret = bfx2.candles(symbol=symbol, TimeFrame=TimeFrame, Section='hist', start=str(start), end=str(end), limit=limit,
                           sort=-1)
        if ret is not None:
            if dataframe:
                df = pd.DataFrame(ret, columns=['Timestamp_orgin', 'Open', 'Close', 'High', 'Low', 'Volume'])
                df['Timestamp'] = df['Timestamp_orgin'].apply(lambda x: x / 1000)
                df['candle_begin_time'] = df['Timestamp'].apply(lambda x: timestamp_to_Localtime(x))
                return df
            else:
                return [{
                    "Timestamp": int(k[0] / 1000),  # MTS
                    "Open": k[1],  # OPEN
                    "High": k[3],  # CLOSE
                    "Low": k[4],  # HIGH
                    "Close": k[2],  # LOW
                    "Volume": k[5],  # VOLUME
                }
                    for k in ret
                ]
        else:
            return None
    elif Section == 'last':
        ret = bfx2.candles(symbol=symbol, TimeFrame=TimeFrame, Section='last')
        if ret is not None:
            return {
                "Timestamp": int(ret[0] / 1000),  # MTS
                "Open": ret[1],  # OPEN
                "High": ret[3],  # CLOSE
                "Low": ret[4],  # HIGH
                "Close": ret[2],  # LOW
                "Volume": ret[5],  # VOLUME
            }
        else:
            return None