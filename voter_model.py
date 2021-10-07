import math
from numpy import *
import random
import matplotlib.pyplot as plt

#Initialize the matrix with size and density given as arguments
def initialize(size, density):
    num_of_minuses = round((1-density) * size**2)
    places = random.sample(range(size**2), num_of_minuses)

    matrix = ones(shape=(size,size))
    
    place = 0
    for i in range(size):
        for j in range(size):
            if place in places:
                matrix[i][j] = 0
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
    

#Check if matrix is complete
def check_matrix(matrix, size):
    sum = 0
    for i in range(size):
        for j in range(size):
            sum += matrix[i][j]
    return sum
    
    
    
def solve_matrix(size, density):
    matrix = initialize(size, density)
    n = 0
    while check_matrix(matrix, size) not in [0,size**2]:
        matrix = adopt_value(matrix, size)
        n += 1
    return n


def different_densitys():
    densitys = []
    durations = []

    density = 0.1
    while density < 1:
        print(density)
        N = []
        for i in range(100):
            N.append(solve_matrix(10, density))
        durations.append(sum(N)/len(N))
        densitys.append(density)
        density += 0.05
    print(durations)


def different_sizes():
    sizes = []
    durations = []


    for s in range(10):
        size = s+2
        print(size)
        N = []
        for i in range(50):
            N.append(solve_matrix(size, 0.5))

        durations.append(sum(N)/len(N))
        sizes.append(size)
    
    print(durations)
    plt.plot(sizes, durations)
    plt.show()

different_sizes()
