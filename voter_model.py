import math
from numpy import *
import random
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#test
#Initialize the matrix with size and density given as arguments
def initialize(size, density):
    num_of_minuses = round((1-density) * size**2)
    places = random.sample(range(size**2), int(num_of_minuses) )

    matrix = ones(shape=(size,size))
    
    place = 0
    for i in range(size):
        for j in range(size):
            if place in places:
                matrix[i][j] = -1
            place += 1

    return matrix


#Choose a random voter and adopt an value of a random voter.
def adopt_value(matrix, n):
    place =  (random.choice(range(n)), random.choice(range(n)))
    directions = [[-1,0], [0,1], [1, 0], [0, -1]]

    def helper(place, poss_directions):
        dir = random.choice(poss_directions)        
        neighbour = (place[0]-dir[0], place[1]-dir[1])

        if neighbour[0] in [-1, n] or neighbour[1] in [-1, n]:
            poss_directions.remove(dir)
            return helper(place, poss_directions)
        else:
            return neighbour
    
    neig = helper(place, directions)
    matrix[place[0]][place[1]] = matrix[neig[0]][neig[1]]
    return matrix
    

#Check if matrix is complete. Returns the sum of entries divided by the size. So it returns either 1 or -1 if completed. 
def check_matrix(matrix, size):
    sum = matrix.sum() #sum over all elements
    return sum/(size**2)
    
    
# Call adopt_value function until the matrix is completed. 
def solve_matrix(size, density):
    matrix = initialize(size, density)
    n = 0
    while check_matrix(matrix, size) not in [-1, 1]:
        matrix = adopt_value(matrix, size)
        n += 1
    
    return (n, check_matrix(matrix, size))

#This function calculates probabilities as a function of density
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
    plt.plot(densitys, probability, color='r', label='sim')
    plt.show()

#This finds out the consensus time as a function of size
def different_sizes():
    sizes = []
    durations = []
    ratio = []

    for s in range(10):
        size = s+2
        N = []
        for i in range(100):
            N.append(solve_matrix(size, 0.7)[0])
        durations.append(sum(N)/len(N))
        sizes.append(size**2)
    
    nlog = []
    for i in range(len(sizes)):
        size = sizes[i]
        nlog.append(0.27*size**2*math.log(size))
        ratio.append(durations[i]/size**2*math.log(size))

    # Ratio is used to investigate if consensus time and chosen function increase with the same rate.

    print(sizes)
    print(durations)
    print(ratio)
    

    plt.plot(sizes, durations, color='r', label='sim')
    plt.plot(sizes, nlog, color='g', label='nlog')
    plt.show()



#Run this function to obtain data on the probabilities for different densities
different_densitys()

#Run this function to obtain data on consensus time as a function of lattice size. 
#different_sizes()