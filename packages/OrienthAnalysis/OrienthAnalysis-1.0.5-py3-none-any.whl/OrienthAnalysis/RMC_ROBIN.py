#!/usr/bin/env python
# encoding: utf-8
'''
@author: FENG
@contact: WEI_Lingfeng@163.com
@file: DC2M.py
@time: 2019/1/11 15:33
@desc:
'''

import re
import numpy as np
import cv2
from matplotlib import pyplot as plt
import pandas as pd
from ROBIN_A import ROBIN_A as rb
import os

class RMC_ROBIN:
    #count=0
    def __init__(self,name,scale,NU,Nburnable,Nring):
        self.name=name#计算名称
        self.scale=scale+2#栅格行列数，相等情况下
        self.NU=NU
        self.NB=Nburnable
        self.Nring=Nring

    '''
    def count(self):
        print('Total RMC_ANA %d' % (RMC_ANA.count))
    '''

    def read_tally(self):
        flname=self.name+'.Tally'
        fp = open(flname, 'r')  # 读取文件
        text = fp.read()
        return text
        fp.close()
        print('Tally文件读取成功')

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
    def read_power(self):
        flname = self.name + '.burn.power'
        fp = open(flname, 'r')  # 读取文件
        text = fp.read()
        return text
        fp.close()
        print('Tally文件读取成功')

    def Tally_NPOW(self):
        'normalized power'
        L = self.scale
        text = self.read_tally()
        Np = L * L  # 总珊元数
        # 编辑正则表达式
        pattp = [''] * Np
        for i in range(Np):
            pattp[i] = ">." + str(i + 1) + ".>.0.*(\d\.\d*E.\d*).*\d\..*\n"
        pattbu = "Total.*Burnup.*MWD/KgHM.*(\d\.\d{3})"
        bu = re.findall(pattbu, text)
        print('燃耗搜索成功，'+'燃耗总步数为：'+str(len(bu)))
        # 匹配正则表达式
        print(type(bu))
        if len(bu) ==0:
            bu=[0]
        lenbu = len(bu)
        POW_cell = [''] * lenbu  # 每个燃耗步cell_i的功率的集合
        POW = [POW_cell] * Np

        POWff_cell = [''] * lenbu  # 格式化的
        POWff = [POW_cell] * Np
        for i in range(Np):
            POW[i] = re.findall(pattp[i], text)
        del pattp
        del text
        print('功率搜索成功')
        POWf=np.ones((Np,lenbu),dtype=float)
        for i in range(lenbu):
            for j in range(Np):
                POWf[j][i]=float(POW[j][i])
        del POW
        Psum=POWf.sum(0)
        POWS=np.zeros([(L+1)*lenbu,L],dtype=float)
        for i in range(lenbu):
            POWS[(L+1)*i][0]=float(bu[i])
            for j in range(L):
                for k in range(L):
                    POWS[(L+1)*i+j+1][k]=POWf[L*j+k][i]/Psum[i]*312
        del POWf
        print('功率分布归一化成功')
        index = []
        for i in range(lenbu):
            index += ['burnup']
            for j in range(L):
                index += [str(i+1)+'0'+str(j + 1)]
        df=pd.DataFrame(POWS,index)
        df.to_csv(self.name+'.csv',encoding='utf-8')
        print('功率分布已保存为csv格式文件')
        return df
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

    def pown(self,plt_bu_step):
        L = self.scale
        Np = L * L  # 总珊元数
        NB = self.NB
        NU = self.NU
        bustep = plt_bu_step
        Nring=self.Nring
        NT = NU + NB * Nring#总cell数
        lenbu=len(self.burnup())
        SKIPr = 4 + (bustep) * (NT + 6)
        SKIPf = (lenbu - bustep - 1) * (NT + 6)
        df = pd.read_csv(self.name + '.burn.power', delim_whitespace=True, skiprows=SKIPr, skipfooter=SKIPf,
                         index_col=[2], names=[1, 2, 3, 4, 5, 6, 7, 8, 9], )
        pow = np.zeros([23, 23])
        for key, value in df.iterrows():
            temp = df[5][key]
            if type(temp).__name__ == 'Series':
                pow[int(key / L)][key % L-1] = df[6][key].sum()
            else:
                pow[int(key / L)][key % L-1] = df[6][key]
        pown = np.zeros([23, 23])
        psum = pow.sum()
        for i in range(L):
            for j in range(L):
                pown[i][j] = pow[i][j] / psum * (NB + NU)
        return pown

    def burnup(self):

        pattbu = 'Total.Burnup.MWD.KgHM...(\d\.\d{6}E.\d{2})'
        text=self.read_power()
        bu = re.findall(pattbu, text)
        del text
        return bu

    def plt(self,plt_data_np_input,plt_burnup_step):

        bustep=plt_burnup_step
        ximg = 5000  # 图像长和宽
        yimg = 5000
        D = int(yimg * 0.8)  # 组件对边长
        L = D * 2 / np.sqrt(3)  # 组件对角线长
        d = 2 / np.sqrt(3) / (self.scale - 2 + 1 / 3) * D
        l = 2 / np.sqrt(3) * d
        xmid = int(ximg / 2)
        ymid = int(yimg / 2)

        "组件边界"
        Marray = [[xmid + L / 2, ymid], [xmid + L / 4, ymid + D / 2], [xmid - L / 4, ymid + D / 2],
                  [xmid - L / 2, ymid], [xmid - L / 4, ymid - D / 2], [xmid + L / 4, ymid - D / 2]]
        img = np.ones((ximg, yimg, 3), np.uint8) * 255
        Mpts = np.array(Marray, np.int32)
        # mpts = mpts.reshape((-1, 1, 2))
        #cv2.polylines(img, [Mpts], True, (0, 0, 0), 2)

        "珊元绘图"
        # 第一个珊元
        L2 = int(self.scale / 2) * d
        fxmid = xmid - np.sqrt(3) * L2 * np.sqrt(3) / 2  # 中点
        fymid = ymid - np.sqrt(3) * L2 / 2
        marray = [[fxmid + d / 2, fymid - l / 4], [fxmid + d / 2, fymid + l / 4], [fxmid, fymid + l / 2],
                  [fxmid - d / 2, fymid + l / 4], [fxmid - d / 2, fymid - l / 4], [fxmid, fymid - l / 2]]  # 第一个珊元各角点坐标
        vector1 = np.array([[d, 0]] * 6)  # 横向平移向量
        vector2 = np.array([[d / 2, l * 3 / 4]] * 6)  # 斜向平移向量
        plt_data_np = plt_data_np_input  # 转成np数据类型，以便计算
        plt_data = pd.DataFrame(plt_data_np)
        # 由于np小数位数不能完美指定（例如：要求0.000，但在np中只能达到0.0的效果），
        # 而pandas数据格式能够，因此下面使用pandas格式定义格式后再转成text字符串数组，
        # 这里，plt_data重新赋值的原因为：重新定义索引成0-22，原来的索引是lochead-locend

        plt_data_np = plt_data_np.transpose()  # !!!需要转置
        plt_data_np = np.abs(plt_data_np)
        # 颜色区间0至dm
        max=np.max(plt_data_np)

        min = 0
        dm = max
        color = [(0, 0, 0)] * self.scale
        color = [color] * self.scale
        color_data = np.zeros([self.scale, self.scale])
        for i in range(self.scale):
            for j in range(self.scale):
                if plt_data_np[i][j] != 0: color_data[i][j] = (plt_data_np[i][j] - min) / dm
        rb = (122, 160, 255)
        rr = (255, 149, 100)
        for i in range(self.scale):
            color[i] = [tuple(np.add(rb, np.multiply(np.subtract(rr, rb), color_data[i][j]))) for j in
                        range(self.scale)]
        # colorbar

        font = cv2.FONT_HERSHEY_SIMPLEX  # 字体
        for i in range(self.scale):
            plt_data[i] = ["%.3f" % plt_data[i][j] for j in range(self.scale)]
        text = [''] * self.scale
        text = [text] * self.scale
        for i in range(self.scale):
            text[i] = [str(plt_data[i][j]) for j in range(self.scale)]

        # opencv画图模块
        temp=66
        for i in range(self.scale):
            marrayi = np.add(marray, vector2 * i )  # 每行
            for j in range(self.scale):
                marrayij = np.add(marrayi, vector1 * (j ))
                mpts = np.array(marrayij, np.int32)
                if i >= int((self.scale - 1) / 2) and j >= int((self.scale - 1) / 2) and (
                        j <= ((self.scale - 1) - (i - int((self.scale - 1) / 2)) - 1)):
                    cv2.polylines(img, [mpts], True, (0, 255, 255), 2)  # 画线
                    cv2.fillPoly(img, [mpts], color[i ][j ])  # 填充
                    # 添加文字
                    r_text = [fxmid + (i ) * d / 2 + (j ) * d - 5 / 12 * d, fymid + (i ) * l * 3 / 4 + l / 6]
                    r_number=np.add(r_text,[1/5*l,-1/3*l])
                    r_text = [int(r_text[0]), int(r_text[1])]
                    r_number = [int(r_number[0]), int(r_number[1])]
                    r_text = tuple(r_text)
                    r_number = tuple(r_number)
                    cv2.putText(img, text[i ][j ], r_text, font, ximg/3000,  (0, 0, 0), 5, cv2.LINE_AA)
                    cv2.putText(img, str(temp), r_number, font, ximg/3000, (0, 0, 0), 5, cv2.LINE_AA)
                    temp-=1
        bu = self.burnup()
        if bu == 0:
            bu = [0]
        bu = np.array(bu)
        if max>1:
            cv2.putText(img, 'RMC Power distribution at %.2f MWd/kgU burnup step' % float(bu[bustep]),
                        (int(1 / 10 * xmid), int(1 / 10 * ymid)), cv2.FONT_HERSHEY_COMPLEX, ximg / 1100,  (0, 0, 0),
                        int(ximg / 500), cv2.LINE_AA)
            cv2.imshow('RMC Power distribution at ' + str(bu[bustep]) + ' MWd/kgU burnup step', img)
        else:
            cv2.putText(img, 'P(ROBIN)-P(RMC) Power distribution at %.2f MWd/kgU burnup step' % float(bu[bustep]),
                        (int(1 / 10 * xmid), int(1 / 10 * ymid)), cv2.FONT_HERSHEY_COMPLEX, ximg / 1400, (0, 0, 0),
                        int(ximg / 1000), cv2.LINE_AA)
            cv2.imshow('RMC Power distribution at ' + str(bu[bustep]) + ' MWd/kgU burnup step', img)
        key = cv2.waitKey(0)
        if key == 27:  # wait for ESC key to exit
            cv2.destroyAllWindows()
        elif key == ord('s'):  # wait for 's' key to save and exit
            cv2.imwrite(self.name + ' burnup_step=' + str(bu[bustep - 1]) + '.jpg', img,
                        [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            cv2.destroyAllWindows()

    def plt_POW(self,burnup_step):

        import os

        bustep=burnup_step*2
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
        img = np.zeros((ximg, yimg, 3), np.uint8)
        Mpts = np.array(Marray,np.int32)
        #mpts = mpts.reshape((-1, 1, 2))
        cv2.polylines(img, [Mpts], True, (0, 255, 255),2)

        "珊元绘图"
        #第一个珊元
        L2=int(self.scale/2)*d
        fxmid=xmid-np.sqrt(3)*L2*np.sqrt(3)/2#中点
        fymid=ymid-np.sqrt(3)*L2/2
        marray = [[fxmid + d / 2, fymid - l / 4], [fxmid + d / 2, fymid + l / 4], [fxmid, fymid + l / 2],
                  [fxmid - d / 2, fymid + l / 4], [fxmid - d / 2, fymid - l / 4], [fxmid, fymid - l / 2]]#第一个珊元各角点坐标
        vector1=np.array([[d,0]]*6)#横向平移向量
        vector2=np.array([[d/2,l*3/4]]*6)#斜向平移向量
        if os.path.exists(self.name + '.csv') is True:
            print('归一化功率分布数据csv文件已存在')

        else:
            print('正在进行功率归一化计算')
            self.Tally_NPOW()
            print('功率归一化计算成功')
        df = pd.read_csv(self.name + '.csv', header=0, index_col=0)
        print('归一化功率分布数据csv文件读取成功。')
        lochead=str(bustep-1)+'01'#切片索引开头
        locend=str(bustep-1)+'023'#切片索引结尾
        plt_data=df.loc[lochead:locend]#切片

        plt_data_np = np.array(plt_data)#转成np数据类型，以便计算
        plt_data=pd.DataFrame(plt_data_np)
        #由于np小数位数不能完美指定（例如：要求0.000，但在np中只能达到0.0的效果），
        #而pandas数据格式能够，因此下面使用pandas格式定义格式后再转成text字符串数组，
        #这里，plt_data重新赋值的原因为：重新定义索引成0-22，原来的索引是lochead-locend
        print(plt_data_np)
        plt_data_np = plt_data_np.transpose()#!!!需要转置

        print(plt_data_np)
        #颜色区间0至dm
        #max=np.max(plt_data_np)
        min=0
        dm=1.5
        color=[(0,0,0)]*self.scale
        color=[color]*self.scale
        color_data=np.zeros([self.scale,self.scale])
        for i in range(self.scale):
            for j in range(self.scale):
                if plt_data_np[i][j]!=0:color_data[i][j]=(plt_data_np[i][j]-min)/dm
        rb=(10,150,0)
        rr=(0,0,255)
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
        for i in range(self.scale-2):
            marrayi=np.add(marray,vector2*(i+1))#每行
            for j in range(self.scale-2):
                marrayij=np.add(marrayi,vector1*(j+1))
                mpts = np.array(marrayij, np.int32)
                if (i<int(self.scale/2) and j>(int(self.scale/2)-i-2)) or (i>=int(self.scale/2) and j<=3/2*self.scale-i-4):
                    cv2.polylines(img, [mpts], True, (0, 255, 255),2)#画线
                    cv2.fillPoly(img, [mpts],color[i+1][j+1])#填充
                    #添加文字
                    r_text=[fxmid+(i+1)*d/2+(j+1)*d-5/12*d,fymid+(i+1)*l*3/4+l/8]
                    r_text=[int(r_text[0]),int(r_text[1])]
                    r_text=tuple(r_text)
                    cv2.putText(img, text[i+1][j+1], r_text, font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        '''
        bu=df.loc['burnup', '0']
        print(bu)
        if bu==0:
            bu=[0]
        bu=np.array(bu)
        '''
        bu = [0]
        cv2.putText(img, 'RMC Power distribution at ' + str(bu[bustep-2]) + ' MWd/kgU burnup step',
                    (int(1 / 10 * xmid), int(1 / 10 * ymid)), cv2.FONT_HERSHEY_COMPLEX, ximg / 1100, (255, 255, 255),
                    int(ximg / 500), cv2.LINE_AA)
        cv2.imshow('RMC Power distribution at '+str(bu[bustep-2])+' MWd/kgU burnup step', img)
        print(1)
        key=cv2.waitKey(0)
        if key == 27:  # wait for ESC key to exit
            cv2.destroyAllWindows()
        elif key == ord('s'):  # wait for 's' key to save and exit
            cv2.imwrite( self.name+' burnup_step='+str(bu[bustep-1])+'.jpg', img,[int(cv2.IMWRITE_JPEG_QUALITY),100])
            cv2.destroyAllWindows()

        #plt.imshow(img, cmap='gray', interpolation='bicubic')
        #plt.xticks([-500, 500]), plt.yticks([-500, 500])  # to hide tick values on X and Y axis
        #plt.show()
        #print(L)

    def pow_diff(self,ROBIN_bu_step,RMC_bu_step,RBcsvname,symmetry):

        name=RBcsvname#ROBIN_A处理后的csv文件
        dp=rb(name,scale,symmetry)
        powrb=dp.read_power_csv(ROBIN_bu_step)
        powrmc=self.pown(RMC_bu_step)
        pow_diff=np.subtract(powrb,powrmc)
        #pow_diff=np.abs(pow_diff)
        for i in range(self.scale):
            for j in range(self.scale):
                if not (i >= int((self.scale - 1) / 2) and j >= int((self.scale - 1) / 2) and (
                        j <= ((self.scale - 1) - (i - int((self.scale - 1) / 2)) - 1))):pow_diff[i][j]=0
        return pow_diff

if __name__ == '__main__':

    RMC_flname = 'bu_100000_50_200_s=0_40'
    scale=21
    NU=300
    NB=12
    Nring=5

    VVER1000=RMC_ROBIN(RMC_flname,scale,NU,NB,Nring)
    #dp.NPOW()
    #dp.read_NPOW()
    RMC_burnup_step=0
    ROBIN_burnup_step=0
    symmetry=1
    ROBIN2_flname='depletion_contour_fm_d=0.01_O'
    plt_option=0
    if plt_option==0:
        pdiff=VVER1000.pow_diff(ROBIN_burnup_step,RMC_burnup_step,ROBIN2_flname,symmetry)
        VVER1000.plt(pdiff,RMC_burnup_step)
    elif plt_option==1:
        RMC_pown=VVER1000.pown(RMC_burnup_step)
        print(RMC_pown)
        VVER1000.plt(RMC_pown,RMC_burnup_step)
    elif plt_option == 2:
        VVER1000.plt_POW(RMC_burnup_step)
