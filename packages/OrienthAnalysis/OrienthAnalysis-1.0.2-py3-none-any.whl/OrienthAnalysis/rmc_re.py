#!/usr/bin/env python
# encoding: utf-8
'''
@author: FENG
@contact: WEI_Lingfeng@163.com
@file: rmc_re.py
@time: 2019/4/8 19:06
@desc:
'''

import re
import numpy as np
from pow_dist.my_packs.about_time import timeran
import os

class rmcpower:

    def __init__(self,path,scale):
        self._path=path
        self.scale=scale+2
        self.Np = int((scale + int(scale / 2) + 1) / 2 * (int(scale / 2) + 1) * 2 - scale)
        self.text=self.__read_power()
        self.bu=self.__get_bu()
        self.len=len(self.bu)
        self.power=self.__get_power() # 1

        self._2d_power=self.__get_2d_power()#2

        self.n_fuel_pin = self.__get_fuel_pin_number()#3
        self._2d_normailized_p = self.__get_2d_normalized_power()#4
        # self._1d_power=self.__get_1d_power()#5
        # self._1d_normailized_p = self.__get_1d_normalized_power()  # 4
        self.oneSixthP=self.__get_onesixth_power()

        #self.text=self.__get_text()

    def __read_power(self):

        with open(self._path,"r") as f:
            text=f.read()
        f.close()
        return  text

    def __get_bu(self):
        patt="Total Burnup\(MWD/KgHM\): (\d\.\d{6}E.\d{2})"
        bu=re.findall(patt,self.text)
        if bu is not None:
            bu=list(map(float,bu))
            for i in range(len(bu)):
                bu[i] = '%.2f' % float(bu[i])
            return bu
        else:raise Exception("None matched for bu")

    @timeran
    def __get_power(self):
        NP=self.scale*self.scale
        patt="1 > (\d{1,3}) > \d{2,3}\s{13,15}(\d\.\d{6}E.\d{2})\s{8}\d\.\d{6}E.\d{2}\s{8}\d\.\d{6}E.\d{2}\s{8}\d\.\d{6}E.\d{2}"
        match = re.findall(patt, self.text)
        cell=[]
        power_match=[]
        power=np.zeros([self.scale*self.scale*self.len],dtype=float)

        #power=[]

        if match is not None:

            for c,p in match:
                cell.append(c)
                power_match.append(p)
            Ncell=int(len(cell)/self.len)
            for i in range(self.len):
                #power.extend(power_match[i*self.Np:i*self.Np+self.NU])
                for j in range(Ncell):
                    #print(i*self.Np+int(cell[j])-1)
                    power[i*NP+int(cell[j])-1]+=float(power_match[j+i*Ncell])
            #power=np.reshape(power,[self.scale*self.len,self.scale])
            #index=list(map(list.index,[cell[self.NU-1:self.Ncell]]*self.NR,set1))
            return power

        else: raise Exception("nothing matched!")


        #print(NP,len(match))
        #return cell

    def __get_2d_power(self):
        return np.reshape(self.power,[self.scale*self.len,self.scale])

    def __get_onestep_1d_power(self,step):
        return self.power[step*self.scale*self.scale:(step+1)*self.scale*self.scale]

    def __get_onestep_2d_power(self,step):
        return self._2d_power[step*self.scale:(step+1)*self.scale]

    def __get_fuel_pin_number(self):
        scale = self.scale
        n=0

        for i in range(scale):
            for j in range(scale):
                if self.__get_onestep_2d_power(0)[i][j]>0.00001:n+=1
        return n

    def __get_2d_normalized_power(self):
        scale = self.scale
        sum=[]
        for i in range(self.len):
            sum.append(np.sum(self.__get_onestep_2d_power(i)))
        #NP = int((scale + int(scale / 2) + 1) / 2 * (int(scale / 2) + 1) * 2 - scale)
        #sum=np.sum(self._2d_power)
        _2d_nmlz_power=self._2d_power
        for step in range(self.len):
            for j in range(self.scale):
                for k in range(self.scale):
                    _2d_nmlz_power[step*self.scale+j][k]=round(_2d_nmlz_power[step*self.scale+j][k]/sum[step]*self.n_fuel_pin,3)

        return _2d_nmlz_power

    def get_onestep_2d_normalized_power(self, step):

        return self._2d_normailized_p[step * self.scale:(step + 1) * self.scale]
    def __get_1d_error(self):
        #TODO __get_1d_error
        pass

    def __get_1d_normalized_power(self):
        scale = self.scale
        NP = scale * scale
        npw = np.zeros([NP], dtype=float)
        sum = np.sum(self._1d_power)
        for i in range(NP):
            npw[i] = float(self.power[i][0])/sum*self.n_fuel_pin
        return npw

    def __get_onesixth_power(self):
        scale=self.scale
        half=int((scale-2)/2+1)
        n6=int((1+half)/2*half)
        power=np.zeros([n6,self.len],dtype=float)

        for step in range(self.len):
            temp=0
            for i in range(half+1):
                for j in range(half+1):
                    if i>=half-j+1:

                        power[temp][step]=(self._2d_normailized_p[i+step*self.scale][j])
                        temp+=1
        return power

    def get_certainStep_onesixth_power(self,steps):
        if steps:
            lens=len(steps)
            try:
                scale = self.scale
                half = int((scale - 2) / 2 + 1)
                n6 = int((1 + half) / 2 * half)

                steplist=list(map(round,list(steps),[2]*lens))
                power = np.zeros([n6, lens], dtype=float)

                temp=0
                for step in steplist:

                    for i in range(n6):
                        for j in range(self.len):
                            if step==self.bu[j]:
                                power[i][temp]=self.oneSixthP[i][j]
                    temp +=1
                return power
            except ValueError: raise Exception("invalid literal for int() with base 10: %s" % steps)


if __name__=="__main__":
    path=r"C:\Users\feng\PycharmProjects\RMC_ANA\data\bu_100000_50_200_s=0_40.burn.power"
    scale=21

    rmc=rmcpower(path,scale)
    a=rmc._2d_power
    bu=rmc.bu
    nf=rmc.n_fuel_pin
    p2d=rmc._2d_normailized_p
    p6=rmc.oneSixthP

    import pandas as pd

    steps=(0,20,40)
    pow=rmc.get_certainStep_onesixth_power(steps)
    names=list(steps)
    df=pd.DataFrame(pow,columns=names)
    df.to_csv(path+"selected_Onesixth"+".csv",encoding="UTF-8")