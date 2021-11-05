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

for e_index, epsilon in enumerate(eps):
    for m_index, m in enumerate(m_a):
        initial_array = np.random.randint(0,256,N).astype(np.float64)
        for i in range(0,100001):
            ind_i = np.random.randint(0,N-1,1)
            ind_j = np.random.randint(0,N-1,1)

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

            if (i%5000 == 0):
                tit = 'i: ' + str(i) + ' m: ' + str(m) + ' epsilon: ' + str(epsilon)

                plt.figure()
                plt.scatter(plot_x,initial_array)
                plt.title(tit)
                plt.show()

        
