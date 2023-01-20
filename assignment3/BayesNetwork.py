from Graph import Graph
from Singleton import Singleton
from Nodes import *

BLOCKED_PREFIX = "blockage_"
EVACUEE_PREFIX = "evacuee_"

class BayesNetwork(Singleton):
    def __init__(self):
        self.graph = Graph()
        self.childrenDict = {}
        self.parentsDict = {}
        self.weatherNode = None
        self.blockedNodes = []
        self.evacueeNodes = []

    def __str__(self):
        str_bayes = self.weatherNode.__str__()
        for node in self.blockedNodes:
            node_name = node.name.split(BLOCKED_PREFIX)[1]
            str_bayes += "\n\nVERTEX " + node_name[2:] + ":\n"
            str_bayes += node.__str__() + "\n"
            for evacuee in self.evacueeNodes:
                if evacuee.name.split(EVACUEE_PREFIX)[1] == node_name:
                    str_bayes += evacuee.__str__()
                    break
        return str_bayes

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
            self.evacueeNodes.append(evacueeNode)

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

    def get_node(self, node_name: str):
        if BLOCKED_PREFIX in node_name:
            for node in self.blockedNodes:
                if node.name == node_name:
                    return node
        elif EVACUEE_PREFIX in node_name:
            for node in self.evacueeNodes:
                if node.name == node_name:
                    return node
        elif node_name == 'WeatherNode':
            return self.weatherNode

    def get_vars(self):
        all = [self.weatherNode]
        all.append(self.blockedNodes)
        all.append(self.evacueeNodes)
        return all
