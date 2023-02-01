from Graph import Graph
from Vertex import Vertex
import itertools
UNKNOWN = "unknown"

def generateAllStates():
    graph = Graph()
    states = []
    vertices = graph.vertexes
    allBlockableEdges = graph.getAllBlockableEdges()
    allPossibilities = itertools.product([True, False, UNKNOWN], repeat=len(allBlockableEdges))
    for possibility in allPossibilities:
        edgesStatusDict = dict(zip(allBlockableEdges, possibility))
        for vertex in vertices:
            states.append(State(vertex, edgesStatusDict))
    states = removeNonLegalStates(states)
    return states

def removeNonLegalStates(states):
    legalStates = []
    for state in states:
        if checkLegal(state):
            legalStates.append(state)
    return legalStates

def checkLegal(state):
    for edge, blockage in state.blockages.items():
        if blockage is True and state.currentVertex.name == edge.toV:
            return False    #a state is not legal if the current vertex is the destination of a broken edge
        if blockage == UNKNOWN and (state.currentVertex.name == edge.toV or state.currentVertex.name == edge.fromV):
            return False    #a state is not legal if the status is unkown and we are at a neighboring vertex
    return True


class State(object):
    def __init__(self, currentVertex: Vertex, BlockagesStatusDict):
        self.currentVertex = currentVertex
        self.blockages = BlockagesStatusDict
        self.graph = Graph()

    def __str__(self):
        s = "STATE\nCurrent vertex: " + str(self.currentVertex) + "\n{"
        for edge in self.blockages:
            s += edge.name + ": " + str(self.blockages[edge]) + ", "
        return s + "}\n"

    def getActions(self):
        return self.graph.getConnectedEdges(self.currentVertex)
