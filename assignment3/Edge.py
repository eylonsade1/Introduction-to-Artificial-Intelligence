class Edge(object):
    def __init__(self, fromV, toV, weight, name):
        self.fromV = fromV
        self.toV = toV
        self.weight = weight
        self.name = name

    def __str__(self):
        return "[Edge from:{} to: {} weight: {}]\n".format(str(self.fromV), str(self.toV), str(self.weight))
