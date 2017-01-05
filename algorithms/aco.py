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

# TWEAK PARAMETERS HERE
# colonySize gets replaced with number of cities; yields a quicker solution
colonySize = 20
alpha = 1
beta = 3
rho = 0.1
q = 1
maxIterations = 250
pheromoneWeight = (1/colonySize)

class ant:

    def __init__(self):
        currentCity = 0
        nextCity = 0
        pathIndex = 0
        traversedCities = []
        followedPaths = []
        tourLength = 0




# def initializeAntsOnNodes(citiesNo):







if __name__ == '__main__':
    dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'input'))
    inputFiles = parser.get_input_files()
    for file in inputFiles:
        dir = os.path.join(dir_path, file)
        queue = parser.read_file(dir)
        citiesNo = parser.next_number(queue)
        matrix = [[0 for x in range(citiesNo)] for y in range(citiesNo)]
        parser.populate_matrix(citiesNo, queue, matrix)

        colonySize = citiesNo

