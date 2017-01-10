####################################################################
#                    ANT COLONY OPTIMIZATION                       #
# ---------------------------------------------------------------- #
# REFERENCE: http://www.theprojectspot.com/tutorial-post/          #
#            ant-colony-optimization-for-hackers/10                #
####################################################################

import parser
import os
import random
import math
import datetime

class PheromoneMatrix:
    def __init__(self, initPheromone, size):
        self.initPheromone = initPheromone
        self.matrix = [[self.initPheromone for x in range(size)] for row in range(size)]

    def scaleMatrix(self, rho):
        self.matrix = [[x * (1 - rho) for x in row] for row in self.matrix]

class Ant:
    def __init__(self, distance_matrix, pheromone_matrix, beta_matrix, alpha, beta, q):
        self.distance_matrix = distance_matrix
        self.pheromone_matrix = pheromone_matrix
        self.tour = None
        self.alpha = alpha
        self.beta = beta
        self.q = q
        self.graph_size = len(distance_matrix)
        self.beta_matrix = beta_matrix

    def reset(self):
        self.tour = None
    
    def init(self):
        self.tour = []
        self.remaining_cities = list(range(self.graph_size))
        randCityIndex = math.floor(random.random() * self.graph_size)
        self.currentCity = randCityIndex
        self.tour.append(self.currentCity)
        self.remaining_cities.remove(self.currentCity)

    def calculate_probabilities(self, rouletteWheel, cityProbabilities):
        current_pheromone = self.pheromone_matrix.matrix[self.currentCity]
        current_beta_row= self.beta_matrix[self.currentCity]
        for cityIndex in self.remaining_cities:
            toCity = cityIndex
            edge_pheromone = current_pheromone[toCity]
            if self.alpha == 1:
                alpha_component = edge_pheromone
            else:
                alpha_component = edge_pheromone ** self.alpha
            beta_component = current_beta_row[cityIndex]
            cityProbabilities[cityIndex] = alpha_component * beta_component
            rouletteWheel += cityProbabilities[cityIndex]
        return rouletteWheel, cityProbabilities

    def pick_from_probabilities(self, rouletteWheel, cityProbabilities):
        wheelTarget = rouletteWheel * random.random()
        wheelPosition = 0.0
        for cityIndex in self.remaining_cities:
            wheelPosition += cityProbabilities[cityIndex]
            if wheelPosition >= wheelTarget:
                self.currentCity = cityIndex
                self.tour.append(cityIndex)
                self.remaining_cities.remove(cityIndex)
                return

    def makeNextMove(self):
        if self.tour == None:
            self.init()

        rouletteWheel = 0.0
        cityProbabilities = [0] * self.graph_size

        rouletteWheel, cityProbabilities = self.calculate_probabilities(rouletteWheel, cityProbabilities)
        self.pick_from_probabilities(rouletteWheel, cityProbabilities)

    def tourFound(self):
        if self.tour == None:
            return False
        return len(self.tour) >= self.graph_size

    def run(self):
        self.reset()
        while not self.tourFound():
            self.makeNextMove()

    def addPheromone(self, weight=1):
        extra_pheromone = (self.q * weight) / self.tour_distance()
        for tourIndex in range(len(self.tour)):
            if tourIndex == len(self.tour)-1:
                fromCity = self.tour[tourIndex]
                toCity = self.tour[0]
            else:
                fromCity = self.tour[tourIndex]
                toCity = self.tour[tourIndex+1]
            edge_pheromone = self.pheromone_matrix.matrix[fromCity][toCity]
            self.pheromone_matrix.matrix[fromCity][toCity] = edge_pheromone + extra_pheromone

    def tour_distance(self):
        length = 0
        for k in range(1, len(self.tour)):
            length = length + self.distance_matrix[self.tour[k-1]][self.tour[k]]
        length = length + self.distance_matrix[self.tour[-1]][self.tour[0]]
        return length

class AntColony:
    def __init__(self, distance_matrix):
        self.colony = []
        self.distance_matrix = distance_matrix
        self.pheromone_matrix = None

        # Set default params
        self.colonySize = 20
        self.alpha = 1
        self.beta = 5
        self.rho = 0.5
        self.q = 1
        self.initPheromone = self.q
        self.type = 'acs'
        self.elitistWeight = 0
        self.maxIterations = 250
        self.minScalingFactor = 0.001

        self.iteration = 0
        self.minPheromone = None
        self.maxPheromone = None

        self.iterationBest = None
        self.globalBest = None

        self.beta_matrix = [[(1.0 / x) ** self.beta if x !=0 else 1 for x in row] for row in distance_matrix]

        self.setInitialPheromone()
        self.createAnts()

    def createAnts(self):
        self.colony = [Ant(self.distance_matrix, self.pheromone_matrix, self.beta_matrix, self.alpha, self.beta, self.q) for i in range(self.colonySize)]

    def reset(self):
        self.iteration = 0
        self.globalBest = None
        self.resetAnts()
        self.setInitialPheromone(self.initPheromone)

    def setInitialPheromone(self):
        self.pheromone_matrix = PheromoneMatrix(self.initPheromone, len(self.distance_matrix))

    def resetAnts(self):
        self.createAnts()
        self.iterationBest = None

    def run(self):
        self.iteration = 0
        while self.iteration < self.maxIterations:
            # if self.getGlobalBest() != None:
            #     print(self.getGlobalBest().tour_distance())
            #     print(datetime.datetime.now())
            self.step()
    
    def step(self):
        # RESTART ANTS AT BEGINNING POSITION
        self.resetAnts()

        for antIndex in range(len(self.colony)):
            # RUN INDIVIDUAL ANTS (REFER TO ANT CLASS)
            self.colony[antIndex].run()

        self.getGlobalBest()
        # AFTER ALL ANTS HAVE COMPLETE TOURS, ADD PHEROMONES
        self.updatePheromone()
        # pretty_print(self.pheromone_matrix.matrix)

        self.iteration = self.iteration + 1

    def updatePheromone(self):
        self.pheromone_matrix.scaleMatrix(self.rho)

        if self.type == 'maxmin':
            if self.iteration / self.maxIterations > 0.75:
                best = self.getGlobalBest()
            else:
                best = self.getIterationBest()
            
            # Set maxmin
            self.maxPheromone = self.q / best.tour_distance()
            self.minPheromone = self.maxPheromone * self.minScalingFactor

            best.addPheromone()
        else:
            for antIndex in range(len(self.colony)):
                self.colony[antIndex].addPheromone()

        if self.type == 'elitist':
            self.getGlobalBest().addPheromone(self.elitistWeight)

        if self.type == 'maxmin':
            [[min(max(x, self.minPheromone), self.maxPheromone) for x in row] for row in self.pheromone_matrix.matrix]
    
    def getIterationBest(self):
        if self.colony[0].tour == None:
            return None

        if self.iterationBest == None:
            best = self.colony[0]
            for antIndex in range(len(self.colony)):
                if best.tour_distance() >= self.colony[antIndex].tour_distance():
                    self.iterationBest = self.colony[antIndex]

        return self.iterationBest

    def getGlobalBest(self):
        # FIND THE BEST RESULTS ACROSS ALL ANTS
        bestAnt = self.getIterationBest()
        if bestAnt == None and self.globalBest == None:
            return None

        if bestAnt != None:
            if self.globalBest == None or self.globalBest.tour_distance() >= bestAnt.tour_distance():
                self.globalBest = bestAnt

        return self.globalBest

def aco(distance_matrix):
    # ALGORITHM BEGINS HERE
    ac = AntColony(distance_matrix)
    ac.run()
    bestAnt = ac.getGlobalBest()
    return bestAnt.tour, bestAnt.tour_distance()

def iterated_aco(matrix, itercount):
    min_length = float("inf")
    min_tour = []
    for i in range(itercount):
        tour, length = aco(matrix)
        if length < min_length:
            min_length = length
            min_tour = tour
    return min_tour, min_length   

def pretty_print(matrix):
    output = ""
    for row in matrix:
        for el in row:
            output += "{0:.2f} ".format(el)
        output += "\n"
    print(output)

if __name__ == '__main__':
    in_dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'input'))
    out_dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'TourfileB'))
    inputFiles = parser.get_input_files('input')
    for file in inputFiles:
        input_url = os.path.join(in_dir_path, file)
        output_url = os.path.join(out_dir_path, "tour" + file)
        queue = parser.read_file(input_url)
        citiesNo = parser.next_number(queue)
        matrix = [[0 for x in range(citiesNo)] for y in range(citiesNo)]
        parser.populate_matrix(citiesNo, queue, matrix)
        print(input_url)
        tour, length = iterated_aco(matrix, 1)
        if sorted(tour) != list(range(len(tour))):
            raise Exception("Misformed tour")
        f = open(output_url, "w")
        f.write("NAME = " + file[:-4] + ",\n")
        f.write("TOURSIZE = " + str(len(tour)) + ",\n")
        f.write("LENGTH = " + str(length) + ",\n")
        f.write(", ".join(map(str, [x + 1 for x in tour])))
        f.close()
        print(tour)
        print(length)


