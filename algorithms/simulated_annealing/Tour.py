class Tour:

    def __init__(self):
        tour_sequence = []

    def addCity(self, city):
        self.tour_sequence.append(city)

    def getCity(self, city):
        return self.tour_sequence[city]

    def lengthOfTour(self):
        return len(self.tour_sequence)