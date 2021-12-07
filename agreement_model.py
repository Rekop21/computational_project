import numpy as np
import matplotlib.pyplot as plt
import math
import random

from numpy.core.function_base import linspace


#Value between 0 and 256 (limits)
#1. Assign opinion to individuals (N>2500)
#2. Choose two individuals i and j
#3. Assume that O_i > O_j
#4. If O_i - O_j < eps
#5. Increase O_j by (m/2)*(O_i-O_j)
#6. Decrease O_i by (m/2)*(O_i-O_j)

eps = [10,50,100]
m_a = [0.3,0.6]
N = 2600
plot_x = linspace(0,2600,2600)

        
fig,ax = plt.subplots(3,4,figsize=(9,5),sharey=True,sharex= True)
subjdict = {}
tvals_all = [[0,300000,500000,1000000],[0,20000,50000,1000000],[0,20000,50000,1000000]]
    
subjids = np.random.randint(0,N,10)

rowind = 0
for e_index, epsilon in enumerate(eps):
    
    subjdict[e_index] = {}
    tvals = tvals_all[e_index]
    print(tvals)
    
    for m_index, m in enumerate(m_a):
        
        di = {}
        for subj in subjids:
            di[subj] = []
        initial_array = np.random.randint(0,256,N).astype(np.float64)
        axind = 0
        
        for i in range(0,1000001):
            ind_i = np.random.randint(0,N,1)
            ind_j = np.random.randint(0,N,1)

            O_i = initial_array[ind_i]
            O_j = initial_array[ind_j]
            
            if np.abs(O_i-O_j) < epsilon:
                dif = (m/2)*np.abs(O_i-O_j)
                if O_i > O_j:
                    O_i -= dif
                    O_j += dif
                else:
                    O_j -= dif
                    O_i += dif
            
            initial_array[ind_i] = O_i
            initial_array[ind_j] = O_j
                
            for subj in subjids:
                di[subj].append(initial_array[subj])

            if (i%10000 == 0):
                
                tit =  "t = " + str(i)
        
                """
                plt.figure()
                plt.scatter(plot_x,initial_array,s=3)
                plt.title(tit,pad=10,fontsize=16)
                plt.xlim(-1,2600)
                plt.xlabel("subject id")
                plt.ylabel("opinion")
                plt.ylim(0,256)
                plt.show()
                """
                
                if m_index == 0 and i in tvals:
                    print(i)
                    tit =  "t = " + str(i)
                    axx = ax[rowind,axind]
                    axx.scatter(plot_x,initial_array,s=3)
                    axx.set_title(tit,pad=10,fontsize=13)
                    axx.set_xlim(-1,2600)
                    
                    if i ==0:
                        axx.set_ylabel("opinion")
                        axx.text(-1300, 125, r"$\epsilon = $" + str(epsilon), fontsize=15,rotation=90,va='center')
                    axx.set_ylim(0,256)
                    axind += 1
                  
        subjdict[e_index][m_index] = di
    rowind += 1
    
for col in range(4):
    ax[2,col].set_xlabel("subject id")
fig.tight_layout()
fig.subplots_adjust(left=0.2)
#fig.savefig("figs/agreement.pdf") #_" + "e" + str(epsilon) + "_m" + str(m) + ".pdf")


#plotting the timeseries figure
tfig,tax = plt.subplots(2,3,figsize=(8,4),sharey=True,sharex="col")

xlims = [700000,150000,60000]
for e_index in subjdict:
    
    for m_index in subjdict[e_index]:
        
        di = subjdict[e_index][m_index]
        #print(di.keys())
        taxx = tax[m_index,e_index]
        
        for subj in di:
            vals = di[subj]
            taxx.plot(np.arange(0,len(vals)),vals)
            taxx.set_ylim(0,256)
            taxx.set_xlim(0,xlims[e_index])

for row in range(len(m_a)):
    
    tax[row,0].set_ylabel("opinion")
    tax[row,0].text(-350000, 125, r"$m = $" + str(m_a[row]), fontsize=16,rotation=90,va='center')
    
for col in range(3):
    
    tax[1,col].set_xlabel("timestep")
    tax[1,col].tick_params('x',labelrotation=40)
    
    title = r"$\epsilon = $" + str(eps[col]) # + ", " +r"$m = $" + str(m)
    tax[0,col].set_title(title ,pad = 10,fontsize=16)
        
tfig.tight_layout()
#plt.subplots_adjust(wspace= 0.1,hspace=0.1,left =0.5,bottom=0.5)
#tfig.savefig("figs/timeseries.pdf")
plt.show()
