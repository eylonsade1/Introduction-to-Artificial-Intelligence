MILD = "mild"
STORMY = "stromy"
EXTREME = "extreme"

class Node(object):
    def __init__(self, probabiliyTable, nodeName):
        self.name = nodeName
        self.table = probabiliyTable

class WeatherNode(Node):
    def __init__(self, probabiliyTable):
        super(WeatherNode, self).__init__(probabiliyTable, "WeatherNode")
        self.legalValues = [MILD, STORMY, EXTREME]

class BlockageNode(Node):
    def __init__(self, probabiliyTable, nodeName):
        super(BlockageNode, self).__init__(probabiliyTable, nodeName)
        self.legalValues = [True, False]

class EvacueeNode(Node):
    def __init__(self, neighobrs, nodeName):
        table = self.generateProbabiliyTable(neighobrs)
        super(EvacueeNode, self).__init__(table, nodeName)
        self.legalValues = [True, False]

    #@todo add caluclation for evacueeNodes
    def generateProbabiliyTable(self, neighborVertexes):
        return []