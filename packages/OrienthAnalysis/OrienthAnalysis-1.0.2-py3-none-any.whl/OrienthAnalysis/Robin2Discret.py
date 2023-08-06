#!/usr/bin/env python
# encoding: utf-8
'''
@author: FENG
@contact: WEI_Lingfeng@163.com
@file: ROBIN2_RM.py
@time: 2019/4/3 12:58
@desc:
'''
#TODO decs
'''
    &&API
    
        class: Robin2Discret
            attributes: scale,...
            

    &&Idea:
    
    Use re module to parse .out file, then get information (power distribution, kinf, keff, fuel temperature, 
    moderator temperature,boron concentration or its text in .out file)of the needed calculation point.
    
    The only difficulty is in arrangement of robin type power distribution to an 2D array:
    
    case 1th: for symmetry=1
    we will change from:
    
         * * * * *
        * * * * * * 
       * * * * * * *
      * * * * * * * *
     * * * * * * * * *
      * * * * * * * *
       * * * * * * *
        * * * * * *
         * * * * *
     
    to:
     - - - - * * * * *
     - - - * * * * * *
     - - * * * * * * *
     - * * * * * * * *
     * * * * * * * * *
     * * * * * * * * -
     * * * * * * * - -
     * * * * * * - - -
     * * * * * - - - -
     
     "*" stand for actual pin power
     "-" stand for inexistent pin
     
    case 2nd: for symmetry=6:
    
     * * * * * 
      * * * * 
       * * *
        * *
         *
         
    to the same shape:
    
     - - - - * * * * *
     - - - * * * * * *
     - - * * * * * * *
     - * * * * * * * *
     * * * * * * * * *
     * * * * * * * * -
     * * * * * * * - -
     * * * * * * - - -
     
     sase 3rd: for symmetry=12:
     
     * * * * *
        * * *  
           *
           
    always the same shape as previous.
'''

import re
import numpy as np
from pow_dist.my_packs.about_time import *


class Robin2Discret:

    '''
    Use re module to parse .out file, then get information (power distribution, kinf, keff, fuel temperature,
    moderator temperature,boron concentration or its text in .out file)of the needed calculation point.
    '''

    def __init__(self,outpath,caltype,scale,symmetry,DEP=None):
        if not isinstance(outpath,str) or not isinstance(caltype,str) or not isinstance(DEP,str):
            raise Exception("class Robin2Discret's attribute must be string type")
        self._path=outpath
        self._type=caltype
        self._DEP=DEP
        self.symmetry=symmetry
        self.scale=scale+2
        self.text = self.__get_text() # read the file then get text
        self.power_dist=self.__get_power_dist()

    def __str__(self):
        return self.cal_type

    __repr__=__str__

    def __init_power_dist(self):
        self.power_dist=self.__get_power_dist()
        #return self._power_dist

    def __read_out(self):
        try:
            with open(self._path,"r") as f:
                text=f.read()
            f.close()
            return  text
        except IOError:
            raise  Exception("IOError:check the file path.")

    @timeran
    def __get_text(self):
        text=self.__read_out()
        if self._DEP is not None:
            patt=self._type+".{60,80}DEP"+"\s{2,3}"+self._DEP+".*?(?:(DEP)|(.*?RRRRRRRRRR))"
        else:
            patt = self._type + ".{60,80}DEP" + "\s{2,3}"+".*?RRRRRRRRRR"
            pass

        match=re.search(patt,text,flags=re.S)
        return match.group()

    @timeran
    def __get_power_dist(self):
        if self.symmetry==1:return self.__get_pd_s1()
        if self.symmetry==6:return self.__get_pd_s6()
        if self.symmetry==12:return self.__get_pd_s12()
        else: raise Exception("symmetry error, 1/6/12 expected")

    def __get_pd_s1(self):
        '''get power_Distribution of whole assembly (symmetry=1)'''
        text=self.text
        L=self.scale
        NP = int((L + int(L / 2) + 1) / 2 * (int(L / 2) + 1) * 2 - L)
        pattp = 'POW(.*?)GRP'
        match=re.search(pattp,text,flags=re.S)

        power1D = np.zeros([NP], dtype=float)
        power2D = np.zeros([L,L], dtype=float)
        if match is not None:
            ''' get every pin power'''
            patt="([0-1]\.\d{3})"
            power_str_list=re.findall(patt,match.group(1),flags=re.S)
            # 2 cases: with number follows "POW" or without.
            if NP != (len(power_str_list) - 1) and NP != (len(power_str_list)):
                raise Exception("symmetry error or file error")
            for i in range(NP):
                if NP == (len(power_str_list) - 1):              # without number behind "POW"
                    power1D[i] = float(power_str_list[i+1])
                if NP == (len(power_str_list)):                  # with number behind "POW", so throw it away
                    power1D[i] = float(power_str_list[i])
            temp=0

            for j in range(L):
                for k in range(L):
                    if ( (L-1-j>int(L/2)) and k >= (int(L / 2 ) - j)) or (
                            j >= int( L / 2 ) and k <= (L+int(L/2)-j-1) ):
                        power2D[j][k] = power1D[temp]
                        temp+=1
        else:
            raise Exception("re. match error, None matched")
        #power_distt
        return power2D


    def __get_pd_s6(self):
        #TODO __get_pd_s6
        pass

    def __get_pd_s12(self):
        #TODO __get_pd_s12
        pass


    def __get_keff(self):
        #TODO __get_keff
        pass

    def __get_kinf(self):
        # TODO __get_kinf
        pass

    def __get_cal_type(self):
        # TODO __get_cal_type
        pass

if __name__=="__main__":
    # parameters necessary:
    outpath=r"D:\实习\data\error_a\restart\depletion_contour_fm_d=0.01_O_RM.out"
    burnup=[0.000,20.000,40.000]
    cal_type=["XEN","SAM",{"TFU":575},{"TMO":300},{"BOR":0}]
    symmetry=1
    scale=21
    #***********************************
    ntype = len(burnup) * len(cal_type)
    power_total=np.zeros([23,23])
    print(power_total)

    typenames=[]
    for i in range(len(cal_type)):
        for j in range(len(burnup)):
            if isinstance(cal_type[i],str):
                typenames.append(cal_type[i]+":"+str(burnup[j]))
            elif isinstance(cal_type[i],dict):
                for key,value in cal_type[i].items():
                    typenames.append(key+str(value)+":"+str(burnup[j]))

        for i in range(len(cal_type)):
            for j in range(len(burnup)):

                single_DEP = str(burnup[j])
                if isinstance(cal_type[i], str):
                    single_type=cal_type[i]
                elif isinstance(cal_type[i], dict):
                    for key in cal_type[i].keys():
                        single_type=key
                #print(i,j,single_type)
                point=Robin2Discret(outpath,single_type,scale,symmetry,single_DEP)
                #print(point.text)
                power_total=np.append(power_total, point.power_dist, axis=0)



    power_total=power_total[scale+2:]
    power_total=power_total.tolist()
    print(power_total)
