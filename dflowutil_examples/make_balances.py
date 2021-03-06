'''
A tutorial on how to make initial conditions for a DFMWAQ model

'''

#import pytest
#import inspect
import os

#dir_tests = os.path.join(os.path.realpath(__file__), os.pardir)
#dir_testoutput = os.path.join(dir_tests,'test_output')
#if not os.path.exists(dir_testoutput):
#    os.mkdir(dir_testoutput)
dir_testinput = os.path.join(r'c:/DATA/werkmap','dfm_tools_testdata')


from dflowutil.SubFile import SubFile
from dflowutil.BalanceFile import BalanceFile
import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns
import pylab
import os
#sns.set()

'''
examine balances
'''

sub_file = os.path.join(dir_testinput,'DSD\\01_substances\\guayas_V11.sub')
bal_file =  os.path.join(dir_testinput,'DSD\\R02\DFM_OUTPUT_current_situation\current_situation_wq_proc_bal.txt') #does not exist
subs = SubFile(sub_file)
prn = BalanceFile(bal_file)
area = ['Domain']
period = ['933-934']
prn.extract_balances(area, period)

'''
now do some plotting
'''

if not os.path.exists(os.path.join(os.path.split(bal_file)[0], 'balances')):
    os.makedirs(os.path.join(os.path.split(bal_file)[0], 'balances'))
    
df = prn.areas
subs = SubFile(sub_file)
for domain in area:
    plt.close('all')
    for sub in subs.substances:
        if subs.transportable[sub] == 'active':
            fig = plt.figure()
            ax = fig.add_axes([0.15,0.3,0.7,0.6])
            print(sub)
            dfi = prn.areas[domain][sub]['Inflows']
            dfo = prn.areas[domain][sub]['Outflows']
            
            x = np.arange(0, len(dfi.columns))
            ax.bar(x, dfi.iloc[0])
            ax.bar(x, -dfo.iloc[0])
            ax.set_ylabel('total mass flux in period')
            plt.title(sub)
            plt.xticks(x, dfi.columns,rotation=90)
            pylab.savefig(os.path.join(os.path.join(os.path.split(bal_file)[0], 'balances'), '%s.png' % sub), dpi = 300)