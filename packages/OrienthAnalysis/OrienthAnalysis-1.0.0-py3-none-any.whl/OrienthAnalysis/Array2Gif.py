#!usr/bin/env python
# encoding: utf-8
'''
@author: feng
@contact: wei_lingfeng@163.com
@file: arraygif.py
@time: 2019/4/28 0:22
@desc:
'''

import numpy as np
import cv2
from matplotlib import pyplot as plt
import imageio
import os
from functools import reduce
from HexLayout import HexLayout
from Rainbow import Rainbow
from EgretH import EgretH 
import sys
import getopt


class Array2Gif:

    def __init__(self,_2d_array:"nstep*np_square_array",burnup:list,path,
                 delpoints:"points to be disappeared"):
        self.array=np.array(_2d_array)
        self.scale=-1
        self.steps=-1
        self.__get_scale()
        self.bu=burnup
        self.nbox=reduce(lambda x,y:x+y,range(int((self.scale-1)/2)))*6+1-6
        #self.delpoints=delpoints
        self.draw_array = HexLayout(self.scale,delpoints)
        self.max=np.max(self.array)
        self.image_dir=os.path.splitext(path)[0]

    def __get_scale(self):
        if len(np.shape(self.array))==2:
            if np.shape(self.array)[0]%np.shape(self.array)[1]==0:
                self.steps=np.shape(self.array)[0]//np.shape(self.array)[1]
                self.scale=np.shape(self.array)[1]
            else:
                raise Exception("%s->%s ->illegal input array, shape(%d,%d)"
                            % (arraygif.__name__,self.__get_scale.__name__,
                               np.shape(self.array)[0],np.shape(self.array)[1]))
        else:
            raise Exception("%s->%s ->the input array is not an 2d array"
                            % (arraygif.__name__,self.__get_scale.__name__))



    def all_to_image(self):
        for i in range(len(self.bu)):
            self.to_image(i,path)

    def to_gif(self,duration):
        images_path=os.listdir(self.image_dir)
        image_before=[]
        for i in range(len(images_path)):
            if images_path[i].endswith("png"):
                image_before.append(int(os.path.splitext(images_path[i])[0]))
        # image_mapping={}
        # for i in range(len(image_before)):
        #     image_mapping.update({float(image_before[i]):image_before[i]})
        # image_f_before=list(map(float,image_before))
        # image_f_before.sort()
        #
        # #os.path.splitext,
        frames=[]
        temp=0
        #for image in images_path:
        #print(image_before)
        image_before.sort()
        #print(image_before)
        for image in image_before:
            temp+=1
            print("reading image %d/%d"%(temp,self.steps))
            images_path=self.image_dir+"\\"+str(image)+".png"
            frames.append(imageio.imread(images_path))

        imageio.mimsave(self.image_dir+"\\"+'1.gif',frames,'GIF',duration=duration)
        print("%s/1.gif saved" % self.image_dir)

    def to_image(self, burnup_step,path):
        bustep = burnup_step
        ximg = 1000  # 图像长和宽
        yimg = 1000

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
        #cv2.polylines(img, [Mpts], True, (0, 0, 0), int(ximg / 1000))

        "珊元绘图"
        # 第一个珊元
        L2 = int(self.scale / 2) * d
        fxmid = xmid - np.sqrt(3) * L2 * np.sqrt(3) / 2  # 中点
        fymid = ymid - np.sqrt(3) * L2 / 2
        marray = [[fxmid + d / 2, fymid - l / 4], [fxmid + d / 2, fymid + l / 4], [fxmid, fymid + l / 2],
                  [fxmid - d / 2, fymid + l / 4], [fxmid - d / 2, fymid - l / 4],
                  [fxmid, fymid - l / 2]]  # 第一个珊元各角点坐标
        vector1 = np.array([[d, 0]] * 6)  # 横向平移向量
        vector2 = np.array([[d / 2, l * 3 / 4]] * 6)  # 斜向平移向量

        plt_data_np = self.array[self.scale*bustep:self.scale*(bustep+1)]
        plt_data = plt_data_np
        # 由于np小数位数不能完美指定（例如：要求0.000，但在np中只能达到0.0的效果），
        # 而pandas数据格式能够，因此下面使用pandas格式定义格式后再转成text字符串数组，
        # 这里，plt_data重新赋值的原因为：重新定义索引成0-22，原来的索引是lochead-locend
        #plt_data_np = plt_data_np.transpose()  # !!!需要转置

        # 颜色区间0至dm
        max = np.max(plt_data_np)


        color5 = (0,0,255)
        color4 = (0,255,255)
        color3 = (0,255,0)
        color2 = (255,255,0)
        color1 = (255,175,0)

        cv2.fillPoly(img, [np.array([[0, 0], [ximg, 0], [ximg, yimg], [0, yimg]],np.int32)], color1)

        colors=[color1,color2,color3,color4,color5]
        a=Rainbow()
        colorbar=a.spectrum(colors,self.nbox)
        colori=[(0,0,0)]*self.scale
        color=[colori]*self.scale

        for i in range(self.scale):
            color[i] = [tuple(colorbar[int(plt_data[i][j]/self.max*(self.nbox-1))]) for j in range(self.scale)]

        font = cv2.FONT_HERSHEY_SIMPLEX  # 字体
        for i in range(self.scale):
            plt_data[i] = ["%.3f" % plt_data[i][j] for j in range(self.scale)]
        text = [''] * self.scale
        text = [text] * self.scale
        for i in range(self.scale):
            text[i] = [str(plt_data[i][j]) for j in range(self.scale)]

        # opencv画图模块
        temp = self.nbox
        for i in range(1,self.scale-1):
            marrayi = np.add(marray, vector2 * i)  # 每行
            for j in range(1,self.scale-1):
                if self.draw_array[i][j]:
                    marrayij = np.add(marrayi, vector1 * (j))
                    mpts = np.array(marrayij, np.int32)
                    cv2.polylines(img, [mpts], True, color1, int(ximg/300))  # 画线
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

        bu = self.bu
        #print(bu)
        cv2.putText(img, "step:"+str(bustep)+'  Time: ' + str(bu[bustep])+"  Max:%.4f" %self.max,
                    (int(3/5*xmid), int(1 / 10 * ymid)), cv2.FONT_HERSHEY_COMPLEX, ximg / 1100, (0, 0, 0),
                    int(ximg / 500), cv2.LINE_AA)
        #cv2.imshow('ROBIN2 Power distribution at ' + str(bu[bustep]) + ' MWd/kgU burnup step', img)
        imagedir=os.path.splitext(path)[0]
        if os.path.exists(imagedir):
            pass
        else:os.mkdir(imagedir)
        cv2.imwrite(imagedir +'\\' + str(bustep) + '.png', img,
                    [int(cv2.IMWRITE_PNG_COMPRESSION), 5])
        print('%s 图片保存成功! 保存路径：'% bu[bustep] + imagedir +'\\' + str(bustep) + '.png')


def usage():

    print(
        "python arragif.py [option]\n \
        -h,--help : print this help message\n \
        -i path   : input file path \
        "
    )

if __name__=="__main__":
    # path=r"C:\Work\Orient_web\orient\nymph\plant\plant_10\unit_1\cycle_1\task_211\.workspace\test_430_1522.out"
    opts,args = getopt.getopt(sys.argv[1:], "-h-i:", ["help"])
    path=""
    for o,v in opts:
        if o in ["-h","--help"]:
            usage()
            sys.exit()
        if o in ["-i"]:
            path=v
    egret = EgretH(path)
    delpoints=[(1,8),(1,15),(8,1),(8,15),(15,1),(15,8)]
    for i in egret.power:
        print(i)
    gifo = Array2Gif(egret.power,egret.burnup,egret.path,delpoints)

    gifo.all_to_image()
    duration=0.01
    gifo.to_gif(duration)
