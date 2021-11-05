import numpy as np
import matplotlib.pyplot as plt
import math
import random

#1. Create lattice with size L
#2. Assign opinion (0,1,3,4,...) to each individuals
#3. Choose one individual and one of its neighbor randomly
#4. If O_i = O_j assign the six neighbours with same opinion
#      A   A        A = assign
#   A O_i O_j A
#      A   A
#the two opinions and initial configurations where one opinion has a majority of 1, 5, and 10 percent. Choose L larger than 50.

L = 60
num_opinions = 4


#Initialize the matrix with L and majority given as arguments
#Modified from voter model
def initialize(L,tot_num_of_opinions):

    matrix = np.random.random_integers(0, tot_num_of_opinions, (L, L))

    return matrix


#Assign six neighbours if same opinion
#Modified from the voter model.
def adopt_opinion(matrix, n):
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
    
    directions = [[-1,0], [0,1], [1, 0], [0, -1]]
    if matrix[place[0]][place[1]] == matrix[neig[0]][neig[1]]:
        for d_index, direct in enumerate(directions): #Adopt value for place's neigbours
            neighbour_2 = (place[0]-direct[0], place[1]-direct[1])

            if neighbour_2[0] in [-1, n] or neighbour_2[1] in [-1, n]: pass
            else: matrix[neighbour_2[0]][neighbour_2[1]] = matrix[place[0]][place[1]]

        for d_index, direct in enumerate(directions): #Adopt value for neig's neigbours
            neighbour_3 = (neig[0]-direct[0], neig[1]-direct[1])

            if neighbour_3[0] in [-1, n] or neighbour_3[1] in [-1, n]: pass
            else: matrix[neighbour_3[0]][neighbour_3[1]] = matrix[neig[0]][neig[1]]

    return matrix



initial_matrix = initialize(L,num_opinions)

for j in range(0,1000001):
    initial_matrix = adopt_opinion(initial_matrix,L)

    if (j%100000 == 0):
        tit = 'number of opinions: '+ str(num_opinions) + ' j: ' + str(j)
        plt.figure()
        plt.matshow(initial_matrix)
        plt.title(tit)
        plt.show()