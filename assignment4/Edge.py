from Vertex import Vertex
class Edge(object):
    def __init__(self, fromV:Vertex, toV:Vertex, weight):
        self.fromV = fromV.name
        self.toV = toV.name
        self.weight = weight
        self.blockageProbability = max(fromV.brokenProb, toV.brokenProb)

    def __str__(self):
        return "[Edge from:{} to: {} weight: {} BlockageProbability: {}]\n".format(self.fromV, self.toV,
                                                                                   self.weight, self.blockageProbability)