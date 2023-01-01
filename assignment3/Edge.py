class Edge(object):
    def __init__(self, fromV, toV, weight):
        self.fromV = fromV
        self.toV = toV
        self.weight = weight

    def __str__(self):
        return "[Edge from:{} to: {} weight: {}]\n".format(str(self.fromV), str(self.toV), str(self.weight))