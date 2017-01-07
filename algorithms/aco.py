####################################################################
#                    ANT COLONY OPTIMIZATION                       #
# ---------------------------------------------------------------- #
# REFERENCE: http://www.theprojectspot.com/tutorial-post/          #
#            ant-colony-optimization-for-hackers/10                #
#            https://ameyajoshi005.wordpress.com/2012/11/10/       #
#            the-traveling-salesman-problem-using-ant-algorithms/  #
####################################################################

import parser
import random
import os

# TWEAK PARAMETERS HERE
class environment:

    def __init__(self, citiesNo):
        """ colonySize gets replaced with number of cities; yields a quicker solution """
        self.colonySize = citiesNo
        # THE WEIGHT OF THE EDGES WITH PHEROMONES
        self.init_pher = (1 / citiesNo)
        # IMPORTANCE OF TRAIL
        self.alpha = 1
        # VISIBILITY
        self.beta = 3
        # EVAPORATION RATE
        self.rho = 0.1
        # THE CONSTANT IN THE FORMULA
        self.q = 100
        # MAX ITERATIONS OF SIMULATION
        self.maxIterations = 250
        self.elitistACO = 1

        # LIST OF ANTS
        self.ants = []
        # INITIALIZE GRAPH WITH PHEROMONES
        self.pheromoneMatrix = [[self.init_pher for x in range(citiesNo)] for y in range(citiesNo)]
        self.bestTourLength = 0
        self.bestIndex = 0

class ant:

    def __init__(self):
        # INDICES OF THE CURRENT AND NEXT CITIES
        self.currentCity = 0
        self.nextCity = 0
        self.pathIndex = 0
        self.traversedCities = [0 for x in range(citiesNo)]
        self.pathTaken = [-1 for x in range(citiesNo)]
        self.tourLength = 0

def initializeSimulation(environment, citiesNo):

    nextCity = 0

    # INITIALIZE ONE ANT ON EACH CITY
    for initAnt in range(0, environment.colonySize):
        nextCity += 1

        if nextCity == citiesNo:
            nextCity = 0

        (environment.ants).append(ant())

        (environment.ants[initAnt]).currentCity = nextCity

        (environment.ants[initAnt]).pathIndex = 1
        (environment.ants[initAnt]).pathTaken[0] = (environment.ants[initAnt]).currentCity
        (environment.ants[initAnt]).nextCity = -1
        (environment.ants[initAnt]).tourLength = 0

        # LOAD FIRST CITY INTO TRAVERSED CITIES LIST
        (environment.ants[initAnt]).traversedCities[(environment.ants[initAnt]).currentCity] = 1


def restartAnts(environment, citiesNo):

    destination = 0

    for ant in range(0, environment.colonySize):
        if (environment.ants[ant]).tourLength < environment.bestTourLength:
            environment.bestIndex = ant
            environment.bestTourLength = (environment.ants[ant]).tourLength

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


def antProduct(source, destination, matrix, environment):
    print(pow((environment.pheromoneMatrix)[source][destination], environment.alpha))
    # TODO: FIND OUT WHY THIS RETURNS ZERO DIVISION ERROR
    print(pow((1.0 / (matrix[source][destination])), environment.beta))
    return (pow((environment.pheromoneMatrix)[source][destination], environment.alpha) * pow((1.0 / (matrix[source][destination])), environment.beta))


def chooseNextCity(ant, citiesNo, matrix, environment):

    destination = 0
    denominator = 0
    source = (environment.ants[ant]).currentCity

    for city in range(0, citiesNo):
        if (environment.ants[ant]).traversedCities[city] == 0:
            denominator += antProduct(source, city, matrix, environment)

    assert denominator != 0

    # ROULETTE TO RANDOMLY CHOOSE A CITY TO GO TO NEXT
    while True:
        destination += 1

        if destination >= citiesNo:
            destination = 0

        if (environment.ants[ant]).traversedCities[destination] == 0:
            p = (antProduct(source, destination, matrix, environment)) / denominator
            x = random.random()
            if (x < p):
                break

    return destination


def simulateAnts(citiesNo, matrix, environment):

    moving = 0

    for ant in range(0, environment.colonySize):
        # CHECK IF THERE ARE ANY MORE CITIES TO VISIT
        if ((environment.ants[ant]).pathIndex < citiesNo):
            (environment.ants[ant]).nextCity = chooseNextCity(ant, citiesNo, matrix, environment)
            (environment.ants[ant]).traversedCities[(environment.ants[ant]).nextCity] = 1
            nextPathIndex = (environment.ants[ant]).pathIndex + 1
            (environment.ants[ant]).pathTaken[nextPathIndex] = (environment.ants[ant]).nextCity

            (environment.ants[ant]).tourLength += matrix[(environment.ants[ant]).currentCity][(environment.ants[ant]).nextCity]

            """ Go from last city to the first """
            if (environment.ants[ant]).pathIndex == citiesNo:
                (environment.ants[ant]).tourLength += matrix[(environment.ants[ant]).pathTaken[citiesNo - 1]][(environment.ants[ant]).pathTaken[0]]

            (environment.ants[ant]).currentCity = (environment.ants[ant]).nextCity
            moving += 1

    return moving


def updateTrails(citiesNo):

    flag = 0

    # PHEROMONE EVAPORATION
    for source in range(0, citiesNo):
        for destination in range(0, citiesNo):
            if (source != destination):
                environment.pheromoneMatrix[source][destination] *= (1.0 - environment.rho)

                if environment.pheromoneMatrix[source][destination] < 0:
                    environment.pheromoneMatrix[source][destination] = environment.init_pher

    # ADD PHEROMONE TO THE TRAIL
    for ant in range(0, environment.colonySize):
        for city in range(0, citiesNo):
            if city < (citiesNo - 1):
                source = (environment.ants[ant]).pathTaken[city]
                destination = (environment.ants[ant]).pathTaken[city + 1]
            else:
                source = (environment.ants[ant]).pathTaken[city]
                destination = (environment.ants[ant]).pathTaken[0]

            for k in range(0, citiesNo):
                if source == (environment.ants[environment.bestIndex]).pathTaken[k] and destination == (environment.ants[environment.bestIndex]).pathTaken[k+1]:
                    flag = 1

                if flag == 1:
                    # ELITIST UPDATE
                    environment.pheromoneMatrix[source][destination] += ((environment.q) / (environment.ants[ant]).tourLength + (environment.q / environment.bestTourLength))
                    environment.pheromoneMatrix[destination][source] = environment.pheromoneMatrix[source][destination]

                else:
                    environment.pheromoneMatrix[source][destination] += (environment.q / (environment.ants[ant]).tourLength)
                    environment.pheromoneMatrix[destination][source] = environment.pheromoneMatrix[source][destination]

    for source in range(0, citiesNo):
        for destination in range(0, citiesNo):
            environment.pheromoneMatrix[source][destination] *= environment.rho


#############################################################
#                      MAIN METHOD                          #
#############################################################

if __name__ == '__main__':
    dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'input'))
    inputFiles = parser.get_input_files()
    for file in inputFiles:
        # DEAL WITH PARSING OF MATRIX
        dir = os.path.join(dir_path, file)
        queue = parser.read_file(dir)
        citiesNo = parser.next_number(queue)
        matrix = [[0 for x in range(citiesNo)] for y in range(citiesNo)]
        parser.populate_matrix(citiesNo, queue, matrix)
        # for i in range(0, len(matrix[0])):
        #     print(matrix[i])

        # BEGIN THE ACO ALGORITHM
        createEnv = environment(citiesNo)
        initializeSimulation(createEnv, citiesNo)

        # currentIteration = 0
        # while currentIteration < environment.maxIterations:
        #     currentIteration += 1
        #     if simulateAnts()

        if simulateAnts(citiesNo, matrix, createEnv) == 0:
            updateTrails(citiesNo)
            restartAnts(createEnv, citiesNo)
