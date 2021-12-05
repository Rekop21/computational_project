import math
from numpy import *
import random
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def initialize(size, density):
    num_of_minuses = round((1-density) * size)
    places = random.sample(range(size), int(num_of_minuses) )
    matrix = ones(size)
    for i in range(size):
        if i in places:
            matrix[i] = -1

    return matrix


#Choose a random voter and adopt an value of a random voter. 1d case
def adopt_value(matrix, n):
    place =  random.choice(range(n))
    directions = [1, -1]

    def helper(place, poss_directions):
        dir = random.choice(poss_directions)        
        neighbour = place - dir
        if neighbour in [-1, n]:
            poss_directions.remove(dir)
            return helper(place, poss_directions)
        else:
            return neighbour
    
    neig = helper(place, directions)
    matrix[place] = matrix[neig]
    return matrix

    

#Check if matrix is complete. Returns the sum of entries divided by the size. So it returns either 1 or -1 if completed. 
def check_matrix(matrix, size):
    sum = matrix.sum() #sum over all elements
    return sum/(size)
    
    
# Call adopt_value function until the matrix is completed. 
def solve_matrix(size, density):
    matrix = initialize(size, density)
    n = 0
    while check_matrix(matrix, size) not in [-1, 1]:
        matrix = adopt_value(matrix, size)
        n += 1
    
    return (n, check_matrix(matrix, size))

solve_matrix(4, 0.5)
#
def different_densitys():
    densitys = []
    durations = []
    probability = []

    density = 0.1
    while density < 1:
        N = []
        succesfull_runs = 0 #runs that end because all sites have value 1
        for i in range(40):
            run_results = solve_matrix(10, density)
            N.append(run_results[0])
            if run_results[1] == 1: succesfull_runs += 1

        durations.append(sum(N)/len(N))
        probability.append(succesfull_runs/40)
        densitys.append(density)
        density += 0.1
        
    
    print(densitys)
    print(probability)
    print(durations)


def different_sizes():
    sizes = []
    durations = []
    suhde = []

    for s in range(20):
        n = s+2
        N = []
        for i in range(600):
            N.append(solve_matrix(n, 0.7)[0])
        durations.append(sum(N)/len(N))
        sizes.append(n)
    
    print(sizes)
    print(durations)
    
    #This nlog is used to obtain how the consensustime scale. In the append() parts can put different functions.
    nlog = []
    for i in range(len(sizes)):
        size = sizes[i]
        nlog.append(0.14*size**3)
        suhde.append(durations[i]/(size**3))
    print(suhde)

    plt.plot(sizes, durations, color='r', label='sim')
    plt.plot(sizes, nlog, color='g', label='nlog')
    plt.show()


#Run this function to obtain data on the probabilities for different densities
#different_densitys()

#Run this function to obtain data on consensus time as a function of lattice size. 
different_sizes()