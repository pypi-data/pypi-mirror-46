#!/usr/bin/env python
# encoding: utf-8
'''
@author: FENG
@contact: WEI_Lingfeng@163.com
@file: about_time.py
@time: 2019/4/3 15:39
@desc:
'''

import time
import functools
def timeran(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        print("using function:",func.__name__)
        start=time.clock()
        func(*args,**kwargs)
        end=time.clock()
        #print("time start: ", start)
        print("time used: %.3f ms" % ((end-start)*1000))
        return func(*args,**kwargs)
    return wrapper