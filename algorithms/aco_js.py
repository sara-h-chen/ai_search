dist_matrix
pheromone_matrix

def length_tour(tour, dist_matrix):
    if self._distance != None:
        return self._distance
    # Calculate the length of a tour
    length = 0
    for k in range(1, len(tour)):
        length = length + dist_matrix[tour[k-1]][tour[k]]
    length = length + dist_matrix[tour[-1]][0]
    self._distance = length
    return self.distance_length

def Ant:
    def __init__(self, graph, params):
        this._tour = null;

    def reset(self):
        this._tour = null;
    
    def init(self):
        this._tour = [];
        var randCityIndex = Math.floor(Math.random() * this._graph.size());
        this._currentCity = this._graph.getCity(randCityIndex);
        this._tour.addCity(this._currentCity);

    def getTour(self):
        return this._tour;

    def makeNextMove(self):
        if (this._tour == null) {
            this.init();
        }

        var rouletteWheel = 0.0;
        var cities = this._graph.getCities();

        var cityProbabilities = [];
        for (var cityIndex in cities) {
            if (!this._tour.contains(cities[cityIndex])) {
                var edge = this._graph.getEdge(this._currentCity, cities[cityIndex]);
                if (this._alpha == 1) {
                    var finalPheromoneWeight = edge.getPheromone();
                } else {
                    var finalPheromoneWeight = Math.pow(edge.getPheromone(), this._alpha);
                }
                cityProbabilities[cityIndex] = finalPheromoneWeight * Math.pow(1.0 / edge.getDistance(), this._beta);
                rouletteWheel += cityProbabilities[cityIndex];
            }
        }

        var wheelTarget = rouletteWheel * Math.random();

        var wheelPosition = 0.0;
        for (var cityIndex in cities) {
            if (!this._tour.contains(cities[cityIndex])) {
                wheelPosition += cityProbabilities[cityIndex];
                if (wheelPosition >= wheelTarget) {
                    this._currentCity = cities[cityIndex];
                    this._tour.addCity(cities[cityIndex]);
                    return;
                }
            }
        }

    def tourFound(self):
        if (this._tour == null) {
            return false;
        }
        return (this._tour.size() >= this._graph.size());

    def run(self):
        this.reset();
        while (!this.tourFound()) {
            this.makeNextMove();
        }

    def addPheromone(self, weight):
        if (weight == undefined) {
            weight = 1;
        }

        var extraPheromone = (this._q * weight) / this._tour.distance();
        for (var tourIndex = 0; tourIndex < this._tour.size(); tourIndex++) {
            if (tourIndex >= this._tour.size()-1) {
                var fromCity = this._tour.get(tourIndex);
                var toCity = this._tour.get(0);
                var edge = this._graph.getEdge(fromCity, toCity);
                var pheromone = edge.getPheromone();
                edge.setPheromone(pheromone + extraPheromone);
            } else {
                var fromCity = this._tour.get(tourIndex);
                var toCity = this._tour.get(tourIndex+1);
                var edge = this._graph.getEdge(fromCity, toCity);
                var pheromone = edge.getPheromone();
                edge.setPheromone(pheromone + extraPheromone);
            }
        }

