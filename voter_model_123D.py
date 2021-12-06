import math
from numpy import *
import random
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#test
#Initialize the matrix with size and density given as arguments
def initialize(size, density,dim):
    num_of_minuses = round((1-density) * size**dim)
    places = random.sample(range(size**dim), int(num_of_minuses))

    if dim == 1:
        matrix = ones(size)
        for i in places:
            matrix[i] = -1
        
    elif dim ==2:
        matrix = ones(shape=(size,size))

        place = 0
        for i in range(size):
            for j in range(size):
                if place in places:
                    matrix[i][j] = -1
                place += 1
                
    elif dim ==3:
        matrix = ones((size,size,size))
        place = 0
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    if place in places:
                        matrix[i][j][k] = -1
                    place += 1

    return matrix


#Choose a random voter and adopt a value of a random voter.
def adopt_value(matrix, n, dim):
    
    place = []
    for d in range(dim):
        place.append(random.choice(range(n)))

    if dim == 1:
        directions = [[-1],[1]]
    elif dim == 2:
        directions = [[-1,0],[0,1],[1,0],[0,-1]]
    elif dim == 3:
        directions = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]

    def helper(place, poss_directions,dim):
        vec = random.choice(poss_directions)
        neighbour = []
        for d in range(dim):
            neighbour.append(place[d]-vec[d])
            
        if -1 in neighbour or n in neighbour:
            poss_directions.remove(vec)
            return helper(place, poss_directions,dim)
        else:
            return neighbour
    
    neig = helper(place, directions,dim)
    matrix[tuple(place)] = matrix[tuple(neig)]

    return matrix
    

#Check if matrix is complete. Returns the sum of entries divided by the size. So it returns either 1 or -1 if completed.
def check_matrix(matrix, size, dim):
    sum = matrix.sum() #sum over all elements
    return sum/(size**dim)
    
    
# Call adopt_value function until the matrix is completed.
def solve_matrix(size, density, dim):
    matrix = initialize(size, density, dim)
    n = 0
    while check_matrix(matrix, size, dim) not in [-1, 1]:
        matrix = adopt_value(matrix, size, dim)
        n += 1
    
    return (n, check_matrix(matrix, size, dim))

#This function calculates probabilities as a function of density
def different_densitys(n_runs,rho_step=0.05,dim=2):
    densitys = []
    durations = []
    probability = []

    density = 0
    while density <= 1.0001:
        N = []
        succesfull_runs = 0 #runs that end because all sites have value 1
        for i in range(n_runs):
            run_results = solve_matrix(10, density,dim)
            N.append(run_results[0])
            if run_results[1] == 1:
                succesfull_runs += 1

        durations.append(sum(N)/len(N))
        probability.append(succesfull_runs/n_runs)
        densitys.append(density)
        density += rho_step
        
    return densitys,probability,durations
    
    
def plot_density():

    densitys,probability,durs = different_densitys(50)
    plt.plot(densitys, probability, color='navy', marker ="o")
    plt.xlabel(r"$\rho_0$",fontsize = 14)
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.ylabel("P(consensus of +1)",fontsize=14)
    #plt.savefig("figs/p_consensus.pdf")
    plt.show()
    

#plot_density()

#This finds out the consensus time as a function of size
def different_sizes(dim=2,interval = 2, rho=0.5, upper = 200,nruns=100):

    Ns = []
    durations = []
    ratio = []

    size = 0
    while size < upper:
        size += interval
        print(size)
        vals = []
        for i in range(nruns):
            vals.append(solve_matrix(size, rho, dim)[0])
        durations.append(sum(vals)/len(vals))
        Ns.append(size**dim)

    return Ns,durations,ratio
    
    
Ns1,durations1,ratio1 = different_sizes(dim=1,interval = 10,upper = 140,nruns=50)
Ns2,durations2,ratio2 = different_sizes(dim=2,interval = 2, upper = 14,nruns=50)
Ns3,durations3,ratio3 = different_sizes(dim=3,interval = 1, upper = 10,nruns=50)


def plot_durations(Ns_all, durations_all, rho = 0.5):

    fig,axs = plt.subplots(1,3,figsize=(10,4))
    titles = ["1D","2D","3D"]
    #intervals = [10,2,1]
    #upper = [200,200,8]

    for ax_ind in range(3):
        
        dim = ax_ind +1
        ax = axs[ax_ind]

        #sizes,durations,ratio = different_sizes(dim, intervals[ax_ind], rho, upper[ax_ind])
        Ns,durations = Ns_all[ax_ind],durations_all[ax_ind]
        theoretical = []
        
        for i in range(len(Ns)):
            N = Ns[i]
            
            if dim == 1:
                theoretical.append(0.2*N**3)
            elif dim == 2:
                theoretical.append(0.3*N**2*(math.log(N)))
            elif dim == 3:
                theoretical.append(0.2*N**2*(math.log(N)))
            #ratio.append(durations[i]/size*math.log(size))

        #print(ratio)
        ax.plot(Ns, durations, color='b', label='simulation',marker="o")
        ax.plot(Ns, theoretical, color='g', label='theoretical',marker="o")
        ax.set_ylabel("duration until consensus",fontsize = 14)
        ax.set_xlabel("N",fontsize=14)
        ax.set_title(titles[ax_ind],fontsize=16)

    axs[2].legend(fontsize=14)
    fig.tight_layout()
    #fig.savefig("figs/durations_all.pdf")
    plt.show()
    
plot_durations([Ns1,Ns2,Ns3],[durations1,durations2,durations3],rho = 0.5)


