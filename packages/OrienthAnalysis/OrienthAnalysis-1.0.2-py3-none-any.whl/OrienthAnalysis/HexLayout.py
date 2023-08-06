#!/usr/bin/env python
# encoding: utf-8
'''
@author: feng
@contact: wei_lingfeng@163.com
@file: hex_shape_array.py
@time: 2019/4/28 1:42
@desc:
this module include method Hexlayout that return an 2d ndarray with values 0,1 that 
arranged in assembly layout shape just as follow:
0 0 0 0 0 0 0
0 1 1 1 0 0 0
0 1 1 1 1 0 0
0 0 1 1 1 1 0
0 0 1 1 1 1 0
0 0 0 1 1 1 0
0 0 0 0 0 0 0
'''

import numpy as np

def HexLayout(scale,del_points):
    array=np.zeros([scale,scale])
    for i in range(1,scale-1):
        for j in range(1,scale-1):
            if ( i<scale/2 and j>scale/2-i ) :
                array[i][j]=1
            elif i>scale/2 and j<int(3/2*scale)-i-1:
                array[i][j]=1
            else:
                pass
            if (i,j) in del_points:array[i][j]=0

    return array

if __name__=="__main__":
 
   a=np.zeros([11,11])
   delpoint=[(1,6)]
   a=HexLayout(15,delpoint)
   print(a)
