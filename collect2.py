# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 13:57:39 2015

@author: imanies
"""

from os.path import join, isfile
import subprocess as sp
import h5py # presents HDF5 files as numpy arrays


class Collect:
    '''
def perfCycles(src, exe_files):
    print '\n++++++ PERF EXECUTABLE PROFILING+++++\n'
    sp.call('rm res.*', shell=True)
    for exe in exe_files:
        
        cmd = '3>>res.txt perf stat --repeat 20 -e cycles:u --log-fd 3 ./%s/%s >> res.txt' % (src,exe)
        print 'Executing the perf cmd for exe : ' + exe
        sp.call(cmd, shell=True)

def perfCall(src, exe_files):
    perfCycles(src, exe_files)
    with open('res.txt','r') as f:
        fil = f.read()
    t = [ff.split('cycles')[0].strip(' ').replace(',','') for ff in fil.split(':\n\n')][1::]
    ETs = [float(tt) for tt in t]
    return dict(zip(exe_files, ETs))
    
    with open('file.txt', 'r') as f:
    exe = [line.strip() for line in f]
    '''
    

    def zsimCall(self, src, exe_files, cfg_file):
        self.zdata={}
        print '\n++++++ ZSIM EXECUTABLE PROFILING +++++\n'
        for exe in exe_files:
            
            with open(cfg_file, 'r') as f:
                fil = f.read()
            t=fil.split('command = ',1)[0] + 'command = "'+exe+\
                '";\n};' +fil.split('command = ',1)[1].split('";\n};',1)[1]
            sp.call('rm modif.cfg', shell=True)
            with open('modif.cfg', 'w') as mf:            
                mf.write(t)
            cmd = './../../zsim/build/opt/zsim modif.cfg' 
            print 'Executing ZSim for the exe : %s' % (exe)
            sp.call(cmd, shell=True)
            
            while (not isfile('zsim-ev.h5')):
                print '..waiting for %s...'%(exe)
                       
            self.zdata [exe] = self.zsimCycles('.') 
            cmd = 'mv zsim-ev.h5 cfg_files/%s.h5'%(exe)
            sp.call(cmd, shell=True)
        #df=pd.DataFrame([zdata[0]]).append(pd.DataFrame([zdata[1]])).transpose()
        return self.zdata
    
    def zsimCycles(self, src):
        # Open stats file
        f = h5py.File(src+'/zsim-ev.h5', 'r')
        # Get the single dataset in the file
        dset = f["stats"]["root"]
        procCycles = dset[-1]['procCycles'][0]
        return procCycles
        