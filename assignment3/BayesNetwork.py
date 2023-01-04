from Graph import Graph
from Singleton import Singleton
from Nodes import *

BLOCKED_PREFIX = "blockage_"
EVACUEE_PREFIX = "evacuee_"

#@todo - add str for part1
class BayesNetwork(Singleton):
    def __init__(self):
        self.graph = Graph()
        self.childrenDict = {}
        self.parentsDict = {}
        self.weatherNode = None
        self.blockedNodes = []

    def createWeatherNodes(self):
        self.weatherNode = WeatherNode(self.graph.weather.getProbabilityTable())
        self.addNode(self.weatherNode)

    def createBlockedNodes(self):
        for vertex in self.graph.vertexes:
            blockedVertexNode = BlockageNode(vertex.getProbabilityTable(), BLOCKED_PREFIX+vertex.name)
            self.addNode(blockedVertexNode)
            self.blockedNodes.append(blockedVertexNode)
            self.addRelation(blockedVertexNode, self.weatherNode)

    def createEvacueeNodes(self):
        for vertex in self.graph.vertexes:
            evacueeNode = EvacueeNode(self.graph.getNeighborsList(vertex), EVACUEE_PREFIX+vertex.name)
            self.addNode(evacueeNode)
            for blockedNode in self.blockedNodes:
                blockedNodeVertexName = blockedNode.name.split(BLOCKED_PREFIX)[1]
                if blockedNodeVertexName == vertex.name:
                    self.addRelation(evacueeNode, blockedNode)
                for neighborVertex in self.graph.getNeighborsList(vertex):
                    if blockedNodeVertexName == neighborVertex[0].name:
                        self.addRelation(evacueeNode, blockedNode)


    def addRelation(self, child: Node, parent: Node):
        if child not in self.childrenDict[parent]:
            self.childrenDict[parent].append((child))
        if parent not in self.parentsDict[child]:
            self.parentsDict[child].append((parent))

    def addNode(self, node: Node):
        if not self.childrenDict.get(node):
            self.childrenDict[node] = []
        if not self.parentsDict.get(node):
            self.parentsDict[node] = []