#!/usr/bin/env python
# encoding: utf-8
'''
@author: FENG
@contact: WEI_Lingfeng@163.com
@file: egret-h_out.py
@time: 2019/4/24 16:30
@desc:
This module include only the class EgretH that process the .out file calculated by EGRET-H to
get power distribution as 2d ndarray and AO, cB, burnup versus step as lists.

It needs only receive the path of the .out file.
'''
import re
import numpy as np
import pandas as pd
import os

class EgretH:

    def __init__(self, path):
        self.path = path
        self.text = self.__read_out()
        self.cb = self.__get_cb()
        self.ao = self.__get_AO()
        self.burnup = self.__get_burnup()
        self.power_text = self.__get_power_text()
        self.scale = self.__get_scale()
        self.power = self.__get_power()

    def __read_out(self):
        with open(self.path, "r") as f:
            return f.read()

    def __get_cb(self):
        patt = r"Fixed Boron Concentration = .*?(\d{0,4}\.\d{2})"
        match = re.findall(patt, self.text)
        if match:
            return list(map(float, match))
        else:
            raise Exception("None matched for cB!")

    def __get_AO(self):
        patt = r"Core AO = .*?(.\d{1,2}\.\d{5})"
        match = re.findall(patt, self.text)
        if match:
            return list(map(lambda x: x*100, map(float, match)))
        else:
            raise Exception("None matched for AO!")

    def __get_burnup(self):
        patt = r"Core Average Burnup = .*?(\d{0,6}\.\d{2})"
        match = re.findall(patt, self.text)
        if match:
            return list(map(float, match))
        else:
            raise Exception("None matched for average burnup!")

    def __get_power_text(self):
        patt=r"CC-Pow_Fiss(.*?)END-CC-Pow_Fiss"
        match=re.findall(patt, self.text, flags=re.S)
        if match:
            return match
        else:
            raise Exception("None matched for power_text!")

    def __get_scale(self):
        patt = "\s(\d{1,2})\s"
        match = re.findall(patt, self.power_text[0], flags=re.S)
        if match:
            return int(len(match)/2)
        else:
            raise Exception("None matched for scale!")

    def __get_power(self):

        power = np.zeros([self.scale, self.scale], dtype=float)
        power_tot = np.zeros([1, self.scale], dtype=float)
        patt = r"(\d\.\d{4})"
        for i in range(len(self.power_text)):
            text = self.power_text[i]
            lines = re.findall("(.*?)\n",text)
            selector = True
            i=0
            for line in lines:
                match = re.findall(patt, line)
                if not match or len(match)<2 :
                    #selector = not selector
                    continue
                elif not selector:
                    selector = not selector
                    continue
                else:
                    selector = not selector
                    if i == 0 or i == int(self.scale/2 + 1) - 1 or i == self.scale - 1:
                        match = [0] + match + [0]
                    for j in range(len(match)):

                        if i < int(self.scale/2 + 1) - 1:
                            power[i][-j-1]=match[j]
                        if i >= int(self.scale/2 + 1) - 1:
                            power[i][j]=match[-j-1]
                    i += 1
            power_tot = np.concatenate((power_tot, power), axis=0)
        power_tot = np.delete(power_tot, 0, axis=0)
        return power_tot.tolist()

    def to_excel(self):
        "AO CB BU"
        all=np.concatenate(([self.burnup], [self.cb], [self.ao]), axis=0)
        all=all.transpose()
        df=pd.DataFrame(all, index=None, columns=["burup", "cB", "AO"])
        dir=os.path.splitext(self.path)[0]
        if not os.path.exists(dir):
            os.mkdir(dir)
        filename=dir+"\\"+"results.xlsx"
        df.to_excel(filename, index=False)

def check_normalized_power(step_length: int, arr: np.ndarray):
    scale=np.shape(arr)[1]
    for step in range(step_length-1):
        sum=np.sum(arr[step*scale : (step + 1)*(scale)])
        print(sum)

def usage():

    print(
        "python EgretH.py [option]\n \
        -h,--help : print this help message\n \
        -i path   : input file path \
        "
    )


if __name__=="__main__":
    
    import getopt
    import sys

    opts,argv = getopt.getopt(sys.argv[1:], "-h-i:", ["help"])
    path = ''
    for o,v in opts:
        if o in ["-h","--help"]:
            usage()
            sys.exit()
        if o in ["-i"]:
            path = v
    #path=r"C:\Work\Orient_web\orient\nymph\plant\plant_7\unit_1\cycle_1\task_316\.workspace\real_c1_59_539.out"
    if path:
        egret=EgretH(path)
        egret.to_excel()
        for i in egret.power:
            print(egret.scale)
