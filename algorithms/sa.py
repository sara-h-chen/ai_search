####################################################################
#                    ANT COLONY OPTIMIZATION                       #
# ---------------------------------------------------------------- #
# REFERENCE: http://www.theprojectspot.com/tutorial-post/          #
#            ant-colony-optimization-for-hackers/10                #
#            https://ameyajoshi005.wordpress.com/2012/11/10/       #
#            the-traveling-salesman-problem-using-ant-algorithms/  #
####################################################################

import parser
import os
import random
import math

def three_opt(p, broad=False):
    """In the broad sense, 3-opt means choosing any three edges ab, cd
    and ef and chopping them, and then reconnecting (such that the
    result is still a complete tour). There are eight ways of doing
    it. One is the identity, 3 are 2-opt moves (because either ab, cd,
    or ef is reconnected), and 4 are 3-opt moves (in the narrower
    sense)."""
    n = len(p)
    # choose 3 unique edges defined by their first node
    a, c, e = random.sample(range(n + 1), 3)
    # without loss of generality, sort
    a, c, e = sorted([a, c, e])
    b, d, f = a+1, c+1, e+1

    if broad == True:
        which = random.randint(0, 7) # allow any of the 8
    else:
        which = random.choice([3, 4, 5, 6]) # allow only strict 3-opt

    # in the following slices, the nodes abcdef are referred to by
    # name. x:y:-1 means step backwards. anything like c+1 or d-1
    # refers to c or d, but to include the item itself, we use the +1
    # or -1 in the slice
    if which == 0:
        sol = p[:a+1] + p[b:c+1]    + p[d:e+1]    + p[f:] # identity
    elif which == 1:
        sol = p[:a+1] + p[b:c+1]    + p[e:d-1:-1] + p[f:] # 2-opt
    elif which == 2:
        sol = p[:a+1] + p[c:b-1:-1] + p[d:e+1]    + p[f:] # 2-opt
    elif which == 3:
        sol = p[:a+1] + p[c:b-1:-1] + p[e:d-1:-1] + p[f:] # 3-opt
    elif which == 4:
        sol = p[:a+1] + p[d:e+1]    + p[b:c+1]    + p[f:] # 3-opt
    elif which == 5:
        sol = p[:a+1] + p[d:e+1]    + p[c:b-1:-1] + p[f:] # 3-opt
    elif which == 6:
        sol = p[:a+1] + p[e:d-1:-1] + p[b:c+1]    + p[f:] # 3-opt
    elif which == 7:
        sol = p[:a+1] + p[e:d-1:-1] + p[c:b-1:-1] + p[f:] # 2-opt

    return sol

def modify_3opt(tour):
    return three_opt(tour, True)

def modify_reverse(tour):
    # Pick two cities at random
    pair = random.sample(range(1, len(tour) + 1), 2)
    i = min(pair)
    j = max(pair)

    new_tour = tour[:]
    new_tour[i:j] = tour[j-1:i-1:-1]
    return new_tour

def simulated_annealing(dist_matrix):
    
    # Number of cities
    d = len(dist_matrix)

    # Initial tour
    tour = list(range(1, d))
    random.shuffle(tour)
    tour = [0] + list(tour)

    # Number of steps and cooling schedule
    nsteps = 80000
    Tinit = 13
    Tfinal = .0001

    # geometric schedule
    T = [Tinit * (Tfinal / Tinit) ** (n * 1.0 / nsteps) for n in range(nsteps + 1)]
    # linear schedule
    # T = [Tinit + (Tfinal-Tinit) * (n * 1.0 / nsteps) for n in range(nsteps + 1)]

    lengths = [0] * nsteps
    lengths[0] = length_tour(tour, dist_matrix)
    for n in range(1, nsteps):
        # Do modification on the current tour
        new_tour = modify_3opt(tour)
        # new_tour = modify_reverse(tour)

        # Compute length of new tour
        new_length = length_tour(new_tour, dist_matrix)
        delta = new_length - lengths[n-1]

        # Decide whether or not to accept the new tour
        if delta < 0 or random.random() < math.exp(-delta * 1.0 / T[n]):
            tour = new_tour
            lengths[n] = new_length
        else:
            lengths[n] = lengths[n-1]
    return tour, lengths[-1]

def length_tour(tour, dist_matrix):
    # Calculate the length of a tour
    length = 0
    for k in range(1, len(tour)):
        length = length + dist_matrix[tour[k-1]][tour[k]]
    length = length + dist_matrix[tour[-1]][0]
    return length

def iterated_sa(matrix, iter_count):
    min_length = float("inf")
    min_tour = []
    for i in range(iter_count):
        tour, length = simulated_annealing(matrix)
        if length < min_length:
            # print(tour)
            # if sorted(tour) != list(range(len(tour))):
            #     raise Exception("Misformed tour")
            # print(length)
            min_length = length
            min_tour = tour
    return min_tour, min_length   

def pretty_print(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

if __name__ == '__main__':
    in_dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'input'))
    out_dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'TourfileA'))
    inputFiles = parser.get_input_files('input')
    for file in inputFiles:
        input_url = os.path.join(in_dir_path, file)
        output_url = os.path.join(out_dir_path, "tour" + file)
        queue = parser.read_file(input_url)
        citiesNo = parser.next_number(queue)
        matrix = [[0 for x in range(citiesNo)] for y in range(citiesNo)]
        parser.populate_matrix(citiesNo, queue, matrix)
        tour, length = iterated_sa(matrix, 100)
        if sorted(tour) != list(range(len(tour))):
            raise Exception("Misformed tour")
        f = open(output_url, "w")
        f.write("NAME = " + file[:-4] + ",\n")
        f.write("TOURSIZE = " + str(len(tour)) + ",\n")
        f.write("LENGTH = " + str(length) + ",\n")
        f.write(", ".join(map(str, [x + 1 for x in tour])))
        f.close()
        print(input_url)
        # print(tour)
        # print(length)


