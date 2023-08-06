#!/usr/bin/env python
# encoding: utf-8
'''
@author: feng
@contact: wei_lingfeng@163.com
@file: robin2_nuclide.py
@time: 2019/4/6 19:17
@desc:

This module include class NiclideRobin2 that gets several important nuclide's density versus burnup
from the .out file of ROBIN2 then creat a corresponding .csv file including all density parameters.

The user only need .out path to declare and attribute a NuclideRobin2 instance just as:
    Instance = NuclideRobin2(path)
   
'''
import re
from my_packs.about_time import timeran
import numpy as np
import warnings

class NuclideRobin2:

    def __init__(self,path):
        self._path = path
        self.text = self.__read_out()
        self.bu = self.__get_bu()
        self.U235 = self.__get_U235()
        self.U236 = self.__get_U236()
        self.U238 = self.__get_U238()
        self.Pu239 = self.__get_Pu239()
        self.Pu240 = self.__get_Pu240()
        self.Pu241 = self.__get_Pu241()
        self.Pu242 = self.__get_Pu242()
        self.Sm149 = self.__get_Sm149()
        self.Xe135 = self.__get_Xe135()
        self.Gd155 = self.__get_Gd155()
        self.Gd157 = self.__get_Gd157()
        self.names = np.array(["bu", "U235", "U236", "U238", "Pu239", "Pu240",
                               "Pu241", "Pu242", "Xe135", "Sm149", "Gd155", "Gd157"])

        if self.__check_len():
            self.tot = self.__tot()

    def __read_out(self):
        with open(self._path, "r") as f:
            text = f.read()
            return text

    @timeran
    def __get_bu(self):
        patt = "DEP\s{2,3}(\d{1,2}\.\d{3})"
        match = list(map(float, re.findall(patt, self.text)))
        return match

    def __check_len(self):

        def euqal(a, b):
            if a != b: return False
            else: return True

        check_result=map(euqal, [len(self.bu)]*11, [len(self.U235),
                                                   len(self.U236),
                                                   len(self.U238),
                                                   len(self.Pu239),
                                                   len(self.Pu240),
                                                   len(self.Pu241),
                                                   len(self.Pu242),
                                                   len(self.Xe135),
                                                   len(self.Sm149),
                                                   len(self.Gd155),
                                                   len(self.Gd157)])
        if not all(list(check_result)): warnings.warn("lengths not all equal")
        else: return True

    def __tot(self):
        lens = len(self.bu)
        tot = np.reshape(self.bu, [lens, 1])
        tot = np.concatenate((tot, np.reshape(self.U235, [lens, 1])), axis=1)
        tot = np.concatenate((tot, np.reshape(self.U236, [lens, 1])), axis=1)
        tot = np.concatenate((tot, np.reshape(self.U238, [lens, 1])), axis=1)
        tot = np.concatenate((tot, np.reshape(self.Pu239, [lens, 1])), axis=1)
        tot = np.concatenate((tot, np.reshape(self.Pu240, [lens, 1])), axis=1)
        tot = np.concatenate((tot, np.reshape(self.Pu241, [lens, 1])), axis=1)
        tot = np.concatenate((tot, np.reshape(self.Pu242, [lens, 1])), axis=1)
        tot = np.concatenate((tot, np.reshape(self.Xe135, [lens, 1])), axis=1)
        tot = np.concatenate((tot, np.reshape(self.Sm149, [lens, 1])), axis=1)
        tot = np.concatenate((tot, np.reshape(self.Gd155, [lens, 1])), axis=1)
        tot = np.concatenate((tot, np.reshape(self.Gd157, [lens, 1])), axis=1)

        return tot

    def __get_U235(self):
        patt = "2235\s{2}(\d\.\d{5}E[+-]\d{2})"
        match = list(map(float, re.findall(patt, self.text)))
        return match

    def __get_U236(self):
        patt = "236\s{2}(\d\.\d{5}E[+-]\d{2})"
        match = list(map(float, re.findall(patt, self.text)))
        return match

    def __get_U238(self):
        patt = "8238\s{2}(\d\.\d{5}E[+-]\d{2})"
        match = list(map(float, re.findall(patt, self.text)))
        return match

    def __get_Pu239(self):
        patt = "6239\s{2}(\d\.\d{5}E[+-]\d{2})"
        match = list(map(float, re.findall(patt, self.text)))
        return match

    def __get_Pu240(self):
        patt = "1240\s{2}(\d\.\d{5}E[+-]\d{2})"
        match = list(map(float, re.findall(patt, self.text)))
        return match

    def __get_Pu241(self):
        patt = "1241\s{2}(\d\.\d{5}E[+-]\d{2})"
        match = list(map(float, re.findall(patt, self.text)))
        return match

    def __get_Pu242(self):
        patt = "1242\s{2}(\d\.\d{5}E[+-]\d{2})"
        match = list(map(float, re.findall(patt, self.text)))
        return match

    def __get_Xe135(self):
        patt = "4135\s{2}(\d\.\d{5}E[+-]\d{2})\n"
        match = list(map(float, re.findall(patt, self.text)))
        return match

    def __get_Sm149(self):
        patt = "4149\s{2}(\d\.\d{5}E[+-]\d{2})\n"
        match = list(map(float, re.findall(patt, self.text)))
        return match

    def __get_Gd155(self):
        patt = "2155\s{2}(\d\.\d{5}E[+-]\d{2})\n"
        match = list(map(float, re.findall(patt, self.text)))
        return match

    def __get_Gd157(self):
        patt = "2157\s{2}(\d\.\d{5}E[+-]\d{2})\n"
        match = list(map(float, re.findall(patt, self.text)))
        return match

def usage():

    print(
        "python NuclideRobin2.py [option]\n \
        -h,--help : print this help message\n \
        -i path   : input file path \
        "
    )

if __name__=="__main__":
    # path=r"C:\Work\Orient_web\orient\nymph\plant\plant_10\unit_1\cycle_1\task_211\.workspace\test_430_1522.out"
    import sys, getopt
    opts,args = getopt.getopt(sys.argv[1:], "-h-i:", ["help"])
    path=""
    for o,v in opts:
        if o in ["-h","--help"]:
            usage()
            sys.exit()
        if o in ["-i"]:
            path=v
    #path=r"C:\Users\feng\PycharmProjects\RMC_ANA\data\depletion_contour_fm_d=0.01_O.out"
    a = NuclideRobin2(path)

    import pandas as pd

    df = pd.DataFrame(a.tot, columns=a.names)
    df.to_csv(path + ".csv")
