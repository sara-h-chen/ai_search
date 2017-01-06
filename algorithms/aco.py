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
class environment:

    def __init__(self, citiesNo):
        """ colonySize gets replaced with number of cities; yields a quicker solution """
        self.colonySize = citiesNo
        # THE WEIGHT OF THE EDGES WITH PHEROMONES
        self.pheromoneWeight = (1/citiesNo)
        # IMPORTANCE OF TRAIL
        self.alpha = 1
        # VISIBILITY MODELED BY THE INVERSE OF DISTANCE
        self.beta = 3
        # EVAPORATION RATE
        self.rho = 0.1
        # THE CONSTANT IN THE FORMULA
        self.q = 100
        # MAX ITERATIONS OF SIMULATION
        self.maxIterations = 250

        # LIST OF ANTS
        self.ants = []
        # INITIALIZE GRAPH WITH PHEROMONES
        self.pheromoneMatrix = [[0 for x in range(citiesNo)] for y in range(citiesNo)]
        self.bestTourLength = 0
        self.bestIndex = 0

class ant:

    def __init__(self):
        # INDICES OF THE CURRENT AND NEXT CITIES
        self.currentCity = 0
        self.nextCity = 0
        self.pathIndex = 0
        self.traversedCities = []
        self.pathTaken = []
        self.tourLength = 0

def initializeSimulation(citiesNo):

    thisCity = 0
    nextCity = 0

    # INITIALIZE ONE ANT ON EACH CITY
    for ant in range(0, environment.colonySize):
        if nextCity == environment.colonySize:
            nextCity = 0

        (environment.ants[ant]).currentCity = nextCity + 1

        for city in range(0, citiesNo):
            (environment.ants[ant]).traversedCities[thisCity] = 0
            (environment.ants[ant]).pathTaken[thisCity] = -1

        (environment.ants[ant]).pathIndex = 1
        (environment.ants[ant]).pathTaken[0] = (environment.ants[ant]).currentCity
        (environment.ants[ant]).nextCity = -1
        (environment.ants[ant]).tourLength = 0

        # LOAD FIRST CITY INTO TRAVERSED CITIES LIST
        (environment.ants[ant]).traversedCities[(environment.ants[ant]).currentCity] = 1


def restartAnts(citiesNo):

    # ant = 0
    destination = 0

    for ant in range(0, environment.colonySize):
        if (environment.ants[ant]).tourLength < bestTourLength:
            global bestIndex
            bestTourLength = (environment.ants[ant]).tourLength
            bestIndex = ant

        (environment.ants[ant]).nextCity = -1
        (environment.ants[ant]).tourLength = 0

        for city in range(0, citiesNo):
            (environment.ants[ant]).traversedCities[city] = 0
            (environment.ants[ant]).pathTaken[city] = -1

        if destination == citiesNo:
            destination = 0

        (environment.ants[ant]).currentCity = destination + 1

        (environment.ants[ant]).pathIndex = 1
        (environment.ants[ant]).pathTaken[0] = (environment.ants[ant]).currentCity

        (environment.ants[ant]).traversedCities[(environment.ants[ant]).currentCity] = 1


def evaporate(source, destination, matrix):
    return (pow((environment.pheromoneMatrix)[source][destination], environment.alpha) * pow((1.0 / (matrix[source][destination])), environment.beta))


# def selectNextCity(ant):




if __name__ == '__main__':
    dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'input'))
    inputFiles = parser.get_input_files()
    for file in inputFiles:
        dir = os.path.join(dir_path, file)
        queue = parser.read_file(dir)
        citiesNo = parser.next_number(queue)
        matrix = [[0 for x in range(citiesNo)] for y in range(citiesNo)]
        parser.populate_matrix(citiesNo, queue, matrix)
        # for i in range(0, len(matrix[0])):
        #     print(matrix[i])

