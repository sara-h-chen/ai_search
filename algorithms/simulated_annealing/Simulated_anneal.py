import math

class Simulated_anneal:

    def __init__(self):
        # SET INITIAL STATES
        temp = 10000
        cooling = 0.003

    def calculateAcceptance(self, energy, newEnergy, temperature):
        if (newEnergy < energy) :
            return 1.0
        else:
            return math.exp((energy - newEnergy) / temperature)