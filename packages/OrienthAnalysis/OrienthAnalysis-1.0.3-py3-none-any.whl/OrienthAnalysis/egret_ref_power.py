#!/usr/bin/env python
# encoding: utf-8
'''
@author: FENG
@contact: WEI_Lingfeng@163.com
@file: egret_ref_power.py
@time: 2019/4/26 16:42
@desc:
'''

import pandas as pd
import numpy as np
from functools import *


class reference_power:

    def __init__(self,excel_path):
        self.path=excel_path
        self.df=self.__get_df()
        self.efpd=self.__get_efpd()
        self.scale = self.__get_scale()
        self.power=self.__get_power()
        self._2d_power=self.__get_2d_power()

    def __get_df(self):
        return pd.read_excel(self.path,sheet_name="Qi")
    def __get_efpd(self):
        return list(self.df.columns)[1:]
    def __get_scale(self):
        map_scale = list(map(lambda i: reduce(lambda x, y: x + y, range(i)), range(3, 10)))
        return (map_scale.index(int((len(self.df[self.efpd[0]])-1+6)/6))+3)*2-1+2

    def __get_power(self):
        return np.delete(np.array(self.df),0,axis=1)
    def __get_2d_power(self):
        lenbu=self.power.shape[1]
        _2d_power = np.zeros([self.scale*lenbu, self.scale])
        map_n4line=[]
        specialline=(1,int(self.scale/2 ),self.scale-2)

        for i in range(1,int(self.scale/2+1)):
            if i in specialline:
                map_n4line.append((int((self.scale-2)/2)+1)-2+i-1)
            else:
                map_n4line.append((int((self.scale-2)/2)+1)+i-1)
        map_n4line_reversed=list(reversed(map_n4line))
        map_n4line_reversed.pop(0)
        map_n4line+=map_n4line_reversed
        map_n4line=[0]+map_n4line
        #print()
        for ibu in range(lenbu):

            for i in range(1,self.scale-1):
                if i < self.scale/2:
                    if i in specialline:

                        _2d_power[self.scale*ibu+i][-(map_n4line[i]+2):-2]=self.power[reduce(lambda x,y:x+y,map_n4line[:i]):reduce(lambda x,y:x+y,map_n4line[:i+1]),ibu]
                    else:
                        _2d_power[self.scale*ibu+i][-(map_n4line[i] + 1):-1] = self.power[reduce(lambda x,y:x+y,map_n4line[:i]):reduce(lambda x, y: x + y, map_n4line[:i + 1]),ibu]
                else:
                    if i in specialline:

                        _2d_power[self.scale * ibu + i][2:(map_n4line[i] + 2)] = self.power[reduce(lambda x, y: x + y,
                                                                                                     map_n4line[
                                                                                                     :i]):reduce(
                            lambda x, y: x + y, map_n4line[:i + 1]), ibu]
                        #print(reduce(lambda x, y: x + y, map_n4line[:i]),reduce(lambda x, y: x + y, map_n4line[:i+1]))
                    else:
                        _2d_power[self.scale * ibu + i][1:(map_n4line[i] + 1)] = self.power[reduce(lambda x, y: x + y,
                                                                                                     map_n4line[
                                                                                                     :i]):reduce(
                            lambda x, y: x + y, map_n4line[:i + 1]), ibu]
        return _2d_power