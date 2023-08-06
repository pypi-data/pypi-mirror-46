import numpy as np
import re
import pandas as pd
import os

class Robin2:

    def __init__(self,name,scale,symmetry):
        self.name=name # 计算名称
        self.scale=scale+2 # 栅格行列数，相等情况下
        self.symmetry=symmetry

    def read_out(self):
        flname = self.name
        fp = open(flname, 'r')  # 读取文件
        text = fp.read()
        fp.close()
        return text

    def burnup(self):
        text = self.read_out()
        pattbu = 'DEP\s{2,3}(\d{1,2}\.\d{3})'
        bu = re.findall(pattbu, text)
        if bu:
            for i in range(len(bu)):
                bu[i] = '%.2f' % float(bu[i])
        else:
            bu=["0"]
        return bu

    def pow(self):

        if self.symmetry == 1:
           return self.__NPOW_S1()
        elif self.symmetry == 6:
           return self.__NPOW_S6()
        elif self.symmetry == 12:
           return self.__NPOW_S12()
        else:
            print('对称性输入错误，或者.out文件损坏')
        print('功率归一化计算成功;')

    def __NPOW_S1(self):
        'normalized power FOR 1/6 symmetric assembly'
        L = self.scale
        Np = L * L
        NP = int((L+int(L/2)+1)/2*(int(L/2)+1)*2-L)
        text = self.read_out()
        num=8*NP
        pattp = 'POW([\s\S]{10,'+str(num)+'})GRP.*\n'
        pattbu = '(POW)'
        bu = re.findall(pattbu, text)
        POW = re.findall(pattp, text)
        lenbu = len(bu)
        pow = np.zeros((NP, lenbu), dtype=float)
        for i in range(lenbu):
            for j in range(NP):
                pown = re.findall('(\d\.\d{3})', POW[i])
                if NP != (len(pown)-1) and NP != (len(pown)):
                    raise Exception("对称性错误，请检查")
                if NP == (len(pown) - 1):
                    pow[j][i] = float(pown[j + 1])
                if NP == (len(pown)):
                    pow[j][i] = float(pown[j])

        POWS = np.zeros([L  * lenbu, L], dtype=float)
        for i in range(lenbu):
            temp = 0
            for j in range(L):
                for k in range(L):
                    if ( (L-1-j>int(L/2)) and k >= (int(L / 2 ) - j)) or (
                            j >= int( L / 2 ) and k <= (L+int(L/2)-j-1) ):
                        POWS[L * i + j][k] = pow[temp][i]
                        temp += 1
        df=pd.DataFrame(POWS,index=range(L*lenbu))
        df.to_csv(self.name+".csv",encoding="UTF-8")
        del df
        del pow
        return  POWS.tolist()

    def __NPOW_S6(self):
        'normalized power FOR 1/6 symmetric assembly'
        L = self.scale
        Np=L*L
        NP = int((int(L / 2 + 1) + 1) / 2 * int(L / 2 + 1))
        text = self.read_out()
        pattp = 'POW([\s\S]{10,800})GRP.*\n'
        pattbu = 'DEP..(.\d\.\d{3})'
        bu = re.findall(pattbu, text)
        POW = re.findall(pattp, text)
        lenbu = len(bu)
        pow = np.zeros((NP, lenbu), dtype=float)
        for i in range(lenbu):
            for j in range(NP):
                pown = re.findall('(\d\.\d{3})', POW[i])
                pow[j][i] = float(pown[j+1])
        POWS=np.zeros([L*lenbu,L],dtype=float)
        for i in range(lenbu):
            #POWS[(L)*i][0]=bu[i]
            temp = 0
            for j in range(L):
                for k in range(L):
                    if j>=int((L-1)/2) and k>=int((L-1)/2) and (k <=((L-1)-(j-int((L-1)/2)))):
                        POWS[(L)*i+j][k]=pow[temp][i]
                        temp+=1
        return POWS.tolist()

    def __NPOW_S12(self):
        patt = "POW"
        POW_line = []
        Nline = 0
        L = self.scale
        maxLine = int(((L + 1) / 2 + 1) / 2)
        arraysize = int((L + 1) / 2)

        with open(self.name) as f:
            for line in f:
                Nline += 1
                POW = re.search(patt, line)
                if POW is not None:
                    POW_line.append(Nline)
        f.close()

        lenbu = len(POW_line)
        pow = np.zeros([L, L])
        pow6 = np.zeros([arraysize * lenbu, arraysize])
        patt = "(\d{1,2}\.\d{3})"
        with open(self.name) as f:
            if POW_line:
                for i in range(POW_line[0]):
                    f.__next__()
                for i in range(maxLine):
                    line = f.readline()
                    data = re.findall(patt, line)
                    for j in range(len(data)): data[j] = float(data[j])

                    pow6[i][arraysize - (arraysize - i):arraysize - i] = np.array(data)
                for i in range(arraysize):
                    for j in range(i):
                        pow6[i][j] = pow6[j][i]
                pow[arraysize - 1:L, arraysize - 1:L] = pow6

                '''
                "多燃耗步"
                for i in range(arraysize):
                    for j in range(i):
                        pow[i][j]=pow[j][i]
                df=pd.DataFrame(pow,index=range(L))
                df.to_csv("123.csv",encoding="UTF_8")
                for n in range(len(POW_line)-1):
                    for i in range(POW_line[n+1]):
                        f.__next__()

                    for i in range(maxLine):
                        line = f.readline()
                        data = re.findall(patt, line)
                        print(data)
                '''
        f.close()
        df = pd.DataFrame(pow, index=range(L * lenbu))
        df.to_csv(self.name + ".csv", encoding="UTF-8")
        del df
        return pow.tolist()

if __name__== "__main__":

    ROBIN2_flname = r"D:\实习\data\error_a\敏感性分析\new\d=0.01_q2_fm.out"
    assembly=Robin2(ROBIN2_flname,21,6)
    p=assembly.pow()
    print(p[0:23])