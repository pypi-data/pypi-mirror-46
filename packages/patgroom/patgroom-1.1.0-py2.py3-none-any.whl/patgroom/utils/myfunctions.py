# -*- coding: utf-8 -*-
"""
Description: 
Author     : Groom
Time       : 2018/10/9
File       : myfunctions.py
Version    : V0.1
"""
import time

def tryagain(sleep_second=5, retry=3):
    def decorator(func):
        def wrap(*args, **kwargs):
            for index in range(retry):
                try:
                    ret = func(*args, **kwargs)
                    return ret
                    break
                except Exception as e:
                    print(e)
                    print('sleep %s s....' % sleep_second)
                    time.sleep(sleep_second)

        return wrap

    return decorator