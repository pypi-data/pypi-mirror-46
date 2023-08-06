#!/usr/bin/env python
# encoding: utf-8
'''
@author: FENG
@contact: WEI_Lingfeng@163.com
@file: RMC_RM.py
@time: 2019/4/4 12:40
@desc:
'''

import re
import numpy as np
from pow_dist.my_packs.about_time import timeran
import os

class rmctally:

    def __init__(self,filepath,scale,step):
        self._path=filepath
        self.scale=scale+2
        self.step=step

        self.tally=self.__get_tally() # 1

        self._2d_fisrate=self.__get_2d_fisrate()#2
        self.n_fuel_pin = self.__get_fuel_pin_number()#3
        self._2d_normailized_fr=self.__get_2d_normalized_fisrate()#4
        #self.text=self.__get_text()

    def __read_tally(self):
        try:
            with open(self._path,"r") as f:
                text=f.read()
            f.close()
            return  text
        except IOError:
            raise  Exception("IOError:check the file path.")

    @timeran
    def __get_tally(self):
        text = self.__read_tally()
        NP=self.scale*self.scale
        patt="(\d\.\d{4}E.\d{2})\s{6}(\d\.\d{4}E.\d{2})"
        match = re.findall(patt, text)
        #print(NP,len(match))
        return match

    def __get_2d_fisrate(self):
        scale=self.scale
        NP = scale * scale
        fisrate=np.zeros([scale,scale],dtype=float)
        for i in range(scale):
            for j in range(scale):
                fisrate[i][j]=float(self.tally[scale*i+j][0])
        return fisrate

    def __get_2d_error(self):
        pass

    def __get_fuel_pin_number(self):
        scale = self.scale
        n=0
        for i in range(scale):
            for j in range(scale):
                if self._2d_fisrate[i][j]>0.00001:n+=1
        return n

    def __get_2d_normalized_fisrate(self):
        scale = self.scale
        #NP = int((scale + int(scale / 2) + 1) / 2 * (int(scale / 2) + 1) * 2 - scale)
        sum=np.sum(self._2d_fisrate)
        nfr=np.zeros([scale,scale],dtype=float) #norm. fission rate
        for i in range(scale):
            for j in range(scale):
                nfr[i][j]=self._2d_fisrate[i][j]/sum*self.n_fuel_pin

        return nfr


class powerout:

    def __init__(self):

        pass

    def __get_power(self):
        pass


if __name__=="__main__":

    filepath=r"C:\Robin_V\Depletion VVER1000 NEA_OCED\withrings\RMC\restart\cmp_ref_result\S3_0.rmc.Tally"
    scale=21
    step=1
    tally1=tally(filepath,scale,step)
    print(tally1._2d_normailized_fr)



