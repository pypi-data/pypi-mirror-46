#!/usr/bin/env python
# encoding: utf-8
'''
@author: FENG
@contact: WEI_Lingfeng@163.com
@file: ROBIN_A.py
@time: 2019/1/22 12:41
@desc:
'''


import re
import yaml
import numpy as np
import cv2
from matplotlib import pyplot as plt
import pandas as pd
#from PIL import Image
import os


class ROBIN_A:
    #count=0
    def __init__(self,name,scale,symmetry):
        self.name=name#计算名称
        self.scale=scale+2#栅格行列数，相等情况下
        self.symmetry=symmetry

    '''
    def count(self):
        print('Total RMC_ANA %d' % (RMC_ANA.count))
    '''

    def read_out(self):
        flname=self.name+'.out'
        fp = open(flname, 'r')  # 读取文件
        text = fp.read()
        return text
        fp.close()

    def POW(self):
        L=self.scale
        text=self.read_tally()
        Np=L*L#总珊元数
        '燃耗计算的功率分布数据接口'
        #编辑正则表达式
        pattp=['']*Np
        for i in range(Np):
            pattp[i] = ">."+str(i+1)+".>.0.*(\d\.\d*E.\d*).*\d\..*\n"
        pattbu="Total.Burnup..MWD/KgHM.*\d\.\d{3}"
        bu=re.findall(pattbu,text)

        #匹配正则表达式
        lenbu=len(bu)
        busteps=int(len(bu)/2)
        POW_cell=['']*lenbu#每个燃耗步celli的功率的集合
        POW=[POW_cell]*Np
        for i in range(Np):
            POW[i]=re.findall(pattp[i],text)


        #格式化处理
        fp = open(self.name + '.POW', 'w')
        for i in range(lenbu):
            fp.write(bu[i]+'\n')
            fp.write('\n')
            for j in range(L):
                str1=''
                    #print(POW_L[j][i])
                    #if j>0:  print(POW_L[j-1][i])

                for k in range(L):
                    str1+=POW[j*L+k][i]+'\t'
                    #print(str1)
                fp.write(str1+'\n')
            fp.write('\n')
        fp.close()

    def NPOW_S6(self):
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
        POWS=np.zeros([(L+1)*lenbu,L],dtype=float)
        for i in range(lenbu):
            POWS[(L+1)*i][0]=bu[i]
            temp = 0
            for j in range(L):
                for k in range(L):
                    if j>=int((L-1)/2) and k>=int((L-1)/2) and (k <=((L-1)-(j-int((L-1)/2)))):
                        POWS[(L+1)*i+j+1][k]=pow[temp][i]
                        temp+=1
        index = []
        for i in range(lenbu):
            index += ['burnup']
            for j in range(L):
                index += [str(i)+'0'+str(j +1)]
        df=pd.DataFrame(POWS,index)
        df.to_csv(self.name+'.csv',encoding='utf-8')
        '''
        #Normalization step
        for i in range(lenbu):
            for j in range(Np):
                POWf[j][i] = POWf[j][i]/Psum[i]*312
        POWff_cell = [0] * lenbu
        POWff = [POWff_cell] * Np
        POWfl = POWf.tolist()
        fp = open(self.name + '.NPOW', 'w')
        for i in range(lenbu):
            fp.write(bu[i] + '\n')
            fp.write('\n')
            for j in range(L):

                for k in range(L):
                    POWff[L*j+k][i]= '{:.3f}'.format(POWfl[L*j+k][i])
                    fp.write(str(POWff[L*j+k][i]) + '\t')
                fp.write('\n')
            fp.write('\n')
        fp.close()
            '''

    def NPOW_S1(self):
        'normalized power FOR 1/6 symmetric assembly'
        L = self.scale
        Np = L * L
        NP = int((L+int(L/2)+1)/2*(int(L/2)+1)*2-L)
        text = self.read_out()
        num=8*NP
        print(num)
        pattp = 'POW([\s\S]{10,'+str(num)+'})GRP.*\n'
        pattbu = '(POW)'
        bu = re.findall(pattbu, text)
        POW = re.findall(pattp, text)
        lenbu = len(bu)
        pow = np.zeros((NP, lenbu), dtype=float)
        for i in range(lenbu):
            for j in range(NP):
                pown = re.findall('(\d\.\d{3})', POW[i])
                if NP != (len(pown)-1):
                    print(len(pown))
                    print('Error:请检查对称性')
                    print('BUG位置：第 %d 个燃耗点'% i)
                    quit()
                pow[j][i] = float(pown[j + 1])


        POWS = np.zeros([(L + 1) * lenbu, L], dtype=float)
        for i in range(lenbu):
            POWS[(L + 1) * i][0] = i
            temp = 0
            for j in range(L):
                for k in range(L):
                    if (j<int(L/2+1-1) and k>(int(L/2+1)-j-2)) or (j>=int(L/2+1-1) and k<=L+int(L/2+1)-j-2):
                        POWS[(L + 1) * i + j + 1][k] = pow[temp][i]
                        temp += 1


        index = []
        for i in range(lenbu):
            index += ['burnup']
            for j in range(L):
                index += [str(i) + '0' + str(j + 1)]
        df = pd.DataFrame(POWS, index)
        df.to_csv(self.name + '.csv', encoding='utf-8')

    def read_power_csv(self,burnup_step):
        bustep = burnup_step
        if os.path.exists(self.name + '.csv') is True:
            print('归一化功率分布数据csv文件已存在;')
        else:
            print('正在进行功率归一化计算;')
            if self.symmetry==1:self.NPOW_S1()
            elif self.symmetry==6:self.NPOW_S6()
            #elif self.symmetry == 12: self.NPOW_S12()
            else:print('对称性输入错误，应为1、6、12其中的一个')
            print('功率归一化计算成功;')
        df = pd.read_csv(self.name + '.csv',index_col=0)
        #df = pd.read_csv(self.name + '.csv','rb')
        print('归一化功率分布数据csv文件读取成功;')
        lochead=str(bustep)+'01'#切片索引开头
        locend=str(bustep)+'023'#切片索引结尾
        plt_data=df.loc[lochead:locend]#切片
        pown = np.array(plt_data)#转成np数据类型，以便计算
        return pown

    def burnup(self):
        if os.path.exists(self.name + '.csv') is True:
            print('归一化功率分布数据csv文件已存在;')
        else:
            print('正在进行功率归一化计算;')
            if self.symmetry==1:self.NPOW_S1()
            elif self.symmetry==6:self.NPOW_S6()
            #elif self.symmetry == 12: self.NPOW_S12()
            else:print('对称性输入错误，应为1、6、12其中的一个')
            print('功率归一化计算成功;')
        df = pd.read_csv(self.name + '.csv', header=0, index_col=0)
        bu = df.loc['burnup', '0']
        bu = np.array(bu)
        return bu

    def plt_POW(self,burnup_step):

        bustep=burnup_step
        ximg=1000 #图像长和宽
        yimg=1000

        D=int(yimg*0.8)  #组件对边长
        L=D*2/np.sqrt(3) #组件对角线长
        d=2/np.sqrt(3)/(self.scale-2+1/3)*D
        l=2/np.sqrt(3)*d
        xmid=int(ximg/2)
        ymid=int(yimg/2)

        "组件边界"
        Marray=[[xmid+L/2,ymid],[xmid+L/4,ymid+D/2],[xmid-L/4,ymid+D/2],[xmid-L/2,ymid],[xmid-L/4,ymid-D/2],[xmid+L/4,ymid-D/2]]
        img = np.ones((ximg, yimg, 3), np.uint8)*255
        Mpts = np.array(Marray,np.int32)
        #mpts = mpts.reshape((-1, 1, 2))
        cv2.polylines(img, [Mpts], True, (0, 0, 0),int(ximg/1000))

        "珊元绘图"
        #第一个珊元
        L2=int(self.scale/2)*d
        fxmid=xmid-np.sqrt(3)*L2*np.sqrt(3)/2#中点
        fymid=ymid-np.sqrt(3)*L2/2
        marray = [[fxmid + d / 2, fymid - l / 4], [fxmid + d / 2, fymid + l / 4], [fxmid, fymid + l / 2],
                  [fxmid - d / 2, fymid + l / 4], [fxmid - d / 2, fymid - l / 4], [fxmid, fymid - l / 2]]#第一个珊元各角点坐标
        vector1=np.array([[d,0]]*6)#横向平移向量
        vector2=np.array([[d/2,l*3/4]]*6)#斜向平移向量


        plt_data_np=self.read_power_csv(burnup_step)
        plt_data=pd.DataFrame(plt_data_np)
        #由于np小数位数不能完美指定（例如：要求0.000，但在np中只能达到0.0的效果），
        #而pandas数据格式能够，因此下面使用pandas格式定义格式后再转成text字符串数组，
        #这里，plt_data重新赋值的原因为：重新定义索引成0-22，原来的索引是lochead-locend
        plt_data_np = plt_data_np.transpose()#!!!需要转置


        #颜色区间0至dm
        #max=np.max(plt_data_np)
        min=0
        dm=1.2
        color=[(0,0,0)]*self.scale
        color=[color]*self.scale
        color_data=np.zeros([self.scale,self.scale])
        for i in range(self.scale):
            for j in range(self.scale):
                if plt_data_np[i][j]!=0:color_data[i][j]=(plt_data_np[i][j]-min)/dm
        rb=(122,160,255)
        rr=(255,149,100)
        for i in range(self.scale):
            color[i]=[tuple(np.add(rb,np.multiply(np.subtract(rr,rb),color_data[i][j])))for j in range(self.scale)]
        #colorbar

        font = cv2.FONT_HERSHEY_SIMPLEX  # 字体
        for i in range(self.scale):
            plt_data[i]=["%.3f"%plt_data[i][j]for j in range(self.scale)]
        text=['']*self.scale
        text=[text]*self.scale
        for i in range(self.scale):
            text[i]=[str(plt_data[i][j]) for j in range(self.scale)]

        #opencv画图模块
        temp = 66
        for i in range(self.scale):
            marrayi = np.add(marray, vector2 * i)  # 每行
            for j in range(self.scale):
                marrayij = np.add(marrayi, vector1 * (j))
                mpts = np.array(marrayij, np.int32)
                if i >= int((self.scale - 1) / 2) and j >= int((self.scale - 1) / 2) and (
                        j <= ((self.scale - 1) - (i - int((self.scale - 1) / 2)) - 1)):
                    cv2.polylines(img, [mpts], True, (0, 255, 255), 2)  # 画线
                    cv2.fillPoly(img, [mpts], color[i][j])  # 填充
                    # 添加文字
                    r_text = [fxmid + (i) * d / 2 + (j) * d - 5 / 12 * d, fymid + (i) * l * 3 / 4 + l / 6]
                    r_number = np.add(r_text, [1 / 5 * l, -1 / 3 * l])
                    r_text = [int(r_text[0]), int(r_text[1])]
                    r_number = [int(r_number[0]), int(r_number[1])]
                    r_text = tuple(r_text)
                    r_number = tuple(r_number)
                    cv2.putText(img, text[i][j], r_text, font, ximg / 2500, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(img, str(temp), r_number, font, ximg / 3000, (0, 0, 0), 1, cv2.LINE_AA)
                    temp -= 1

        bu=self.burnup()
        print(bu)
        cv2.putText(img,'Orient_hPowDistPlot Power distribution at '+str(bu[bustep-1])+' MWd/kgU burnup step',(int(1/10*xmid),int(1/10*ymid)), cv2.FONT_HERSHEY_COMPLEX , ximg/1100, (0, 0, 0), int(ximg/500), cv2.LINE_AA)
        cv2.imwrite( self.name+' burnup_step='+str(bu[bustep-1])+'.png', img,[int(cv2.IMWRITE_PNG_COMPRESSION),5])

        return self.name+' burnup_step='+str(bu[bustep-1])+'.png'
        print('图片保存成功')
        '''
        img1 = Image.open(self.name+' burnup_step='+str(bu[bustep-1])+'.png')
        img1 = addTransparency(img1, factor=0.7)
        img1.save(self.name+' burnup_step='+str(bu[bustep-1])+'.png')
        '''

def addTransparency(img, factor=1):
        img = img.convert('RGBA')
        img_blender = Image.new('RGBA', img.size, (0, 0, 0, 0))
        img = Image.blend(img_blender, img, factor)
        return img