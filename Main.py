# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 16:37:09 2015

@author: imanies

"""

import matplotlib.pyplot as pl
import numpy as np
from sklearn import linear_model
from os.path import join, isfile, relpath
from os import listdir, walk
import collect 

def get_mibench(src): 
    exe = []
    for root, dirs, files in walk(src):
        for name in files:
            if name == 'runme_small.sh':
                exe.append(relpath(join(root, name)))
    return exe
    
def get_mala(src):
    return [ f for f in listdir(src) if isfile(join(src,f)) ]
    
def main(src, cfg_h, cfg_t, exe_files): #src is path to executables
    
    host = collect.Collect()
    target = collect.Collect()
    #Execution times of executables run on HOST computer
    hData = host.zsimCall(src, exe_files, cfg_h)

    #Execution times of executables tun on TARGET computer
    tData = target.zsimCall(src, exe_files, cfg_t)
    return hData, tData

def display(data):
    td = np.array(data[1].values())
    hd = np.array(data[0].values())
    regr = linear_model.LinearRegression()
    
    hd_x = hd[:, np.newaxis]
    td_x = td[:, np.newaxis]

    regr.fit(hd_x, td_x)
    
    pl.scatter(hd, td,  color='black')
    pl.plot(hd_x, regr.predict(hd_x), color='red', linewidth=2)
    
    pl.show()
    
    
    '''
    for key, value in d[0].items():
        d[0][key] = value / 1400

    for key, value in d[1].items():
        d[1][key] = value / 2270
    '''