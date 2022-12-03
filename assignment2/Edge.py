class Edge(object):
    def __init__(self, fromV, toV):
        self.fromV = fromV
        self.toV = toV

    def __str__(self):
        return "[Edge from:{} to: {} ]\n".format(str(self.fromV), str(self.toV))