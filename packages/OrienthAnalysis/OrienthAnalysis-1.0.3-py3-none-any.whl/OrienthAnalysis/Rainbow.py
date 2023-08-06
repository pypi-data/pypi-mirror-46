#!/usr/bin/env python
# encoding: utf-8
'''
@author: feng
@contact: wei_lingfeng@163.com
@file: rainbow.py
@time: 2019/4/28 2:21
@desc:
This module include a Rainbow class that makes from several color list 
a list of colors more resolute and of number selected by user.

Instance declaration: ins = Rainbow(ColorList: list, Number: int) 
'''
import numpy as np
class Rainbow:

    def __init__(self):
        pass

    def spectrum(self, colorsource: list, Ncolor: int) -> list :
        if isinstance(colorsource, list):
            if isinstance(Ncolor, int) and Ncolor > 2:
                colorbar = np.zeros([Ncolor, 3])
                Ns = len(colorsource)
                step = Ncolor/(Ns - 1)
                for i in range(Ncolor):
                    x = int(i/step)
                    for icolor in [1,2]:
                        colorbar[i][icolor] = (colorsource[x][icolor]
                                               - (colorsource[x][icolor] - colorsource[x + 1][icolor])*(i/step - x))
                return colorbar
            else:
                raise Exception("int type expected for Ncolor")
        else:
            raise Exception("list type expected for colorsource")

if __name__=="__main__":
    color1 = (255, 0, 0)
    color2 = (255, 255, 0)
    color3 = (0, 255, 0)
    color4 = (0, 255, 255)
    color5 = (0, 175, 255)
    #print(color1[1])
    colors = [color1, color2, color3, color4, color5]

    color=rainbow()
    print(color.spectrum(colors,10)[1])
