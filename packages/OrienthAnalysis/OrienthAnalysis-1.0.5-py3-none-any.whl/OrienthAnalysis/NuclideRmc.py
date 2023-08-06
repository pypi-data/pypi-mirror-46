#!/usr/bin/env python
# encoding: utf-8
'''
@author: feng
@contact: wei_lingfeng@163.com
@file: rmc_nuclide.py
@time: 2019/4/7 16:11
@desc:
'''

'''get every nuclide density versus burnup

'''
import re
from my_packs.about_time import timeran
import numpy as np
import warnings


class NuclideRmc:

    def __init__(self, path,pitch):
        self._path = path
        self._pitch = pitch
        self.volume = pitch / np.sqrt(3) * pitch / 2 / 2 * 6
        self.text = self.__read_dentot()
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
        self.names=np.array(["bu",
                             "U235",
                             "U236",
                             "U238",
                             "Pu239",
                             "Pu240",
                             "Pu241",
                             "Pu242",
                             "Xe135",
                             "Sm149",
                             "Gd155",
                             "Gd157"])

        if self.__check_len():
            self.tot=self.__tot()

    def __read_dentot(self):
        if self._path.endswith("den_tot"):
            with open(self._path, "r") as f:
                text = f.read()
                return text
        else: raise Exception('filename must ends with ".dentot"')

    def correct(self,str):
        return float(str)/self.volume

    def __check_len(self):

        def euqal(a,b):
            if a!=b:return False
            else: return True

        check_result=map(euqal,[len(self.bu)]*11,[len(self.U235),
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
        tot = np.reshape(self.bu,[lens,1])
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

    @timeran
    def __get_bu(self):
        patt = "Total Burnup\(MWD/KgHM\):\s(\d{1}\.\d{6}E[+-]\d{2})"
        match = list(map(float, re.findall(patt, self.text)))
        return match

    def __get_U235(self):
        patt = "U235\s{6}(\d{1}\.\d{6}E[+-]\d{2})"
        match = list(map(self.correct, re.findall(patt, self.text)))
        return match

    def __get_U236(self):
        patt = "U236\s{6}(\d{1}\.\d{6}E[+-]\d{2})"
        match = list(map(self.correct, re.findall(patt, self.text)))
        return match

    def __get_U238(self):
        patt = "U238\s{6}(\d{1}\.\d{6}E[+-]\d{2})"
        match = list(map(self.correct, re.findall(patt, self.text)))
        return match

    def __get_Pu239(self):
        patt = "Pu239\s{5}(\d{1}\.\d{6}E[+-]\d{2})"
        match = list(map(self.correct, re.findall(patt, self.text)))
        return match

    def __get_Pu240(self):
        patt = "Pu240\s{5}(\d{1}\.\d{6}E[+-]\d{2})"
        match = list(map(self.correct, re.findall(patt, self.text)))
        return match

    def __get_Pu241(self):
        patt = "Pu241\s{5}(\d{1}\.\d{6}E[+-]\d{2})"
        match = list(map(self.correct, re.findall(patt, self.text)))
        return match

    def __get_Pu242(self):
        patt = "Pu242\s{5}(\d{1}\.\d{6}E[+-]\d{2})"
        match = list(map(self.correct, re.findall(patt, self.text)))
        return match

    def __get_Xe135(self):
        patt = "Xe135\s{5}(\d{1}\.\d{6}E[+-]\d{2})"
        match = list(map(self.correct, re.findall(patt, self.text)))
        return match

    def __get_Sm149(self):
        patt = "Sm149\s{5}(\d{1}\.\d{6}E[+-]\d{2})"
        match = list(map(self.correct, re.findall(patt, self.text)))
        return match

    def __get_Gd155(self):
        patt = "Gd155\s{5}(\d{1}\.\d{6}E[+-]\d{2})"
        match = list(map(self.correct, re.findall(patt, self.text)))
        return match

    def __get_Gd157(self):
        patt = "Gd157\s{5}(\d{1}\.\d{6}E[+-]\d{2})"
        match = list(map(self.correct, re.findall(patt, self.text)))
        return match


def usage():

    print(
        "python NuclideRmc.py [option]\n \
        -h,--help : print this help message\n \
        -i path   : input file path \
        "
    )

if __name__=="__main__":
    
    import sys, getopt
    
    opts,args = getopt.getopt(sys.argv[1:], "-h-i:", ["help"])
    path=""
    for o,v in opts:
        if o in ["-h","--help"]:
            usage()
            sys.exit()
        if o in ["-i"]:
            path=v
  
    #path = r"C:\Users\feng\PycharmProjects\RMC_ANA\data\r=5_s=0.33.rmc.burn.den_tot"
    pitch = 23.6
    a = NuclideRmc(path, pitch)
    # b = a.bu
    # U236=a.U238
    # Xe=a.Xe135
    # Sm=a.Sm149
    # Gd155=a.Gd155
    # Gd157=a.Gd157
    # print(b)
    # print(Xe)
    # print(Sm)
    # print(len(Gd155),Gd155)
    # print(len(Gd157),Gd157)
    # print(np.reshape(a.U236,[65,1]))
    # print(a.tot)
    import pandas as pd

    df = pd.DataFrame(a.tot, columns=a.names)
    df.to_csv(path + ".csv")


