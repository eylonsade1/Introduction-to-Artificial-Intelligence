from Graph import Graph
from Vertex import Vertex
import itertools

UNKNOWN = "unknown"
GOAL = "goal"


def generateAllStates():
    graph = Graph()
    states = []
    vertices = graph.vertexes
    allBlockableEdges = graph.getAllBlockableEdges()
    allPossibilities = itertools.product([False, True, UNKNOWN], repeat=len(allBlockableEdges))
    for possibility in allPossibilities:
        edgesStatusDict = dict(zip(allBlockableEdges, possibility))
        for vertex in vertices:
            states.append(State(vertex, edgesStatusDict))
    # states = removeNonLegalStates(states)
    return states


def removeNonLegalStates(states):
    legalStates = []
    for state in states:
        if checkLegal(state):
            legalStates.append(state)
    return legalStates


def checkLegal(state):
    for edge, blockage in state.blockages.items():
        # if blockage == True and (state.currentVertex.name == edge.toV or state.currentVertex.name == edge.fromV):
        #     return False  # a state is not legal if the current vertex is the destination of a broken edge
        if blockage == UNKNOWN and (state.currentVertex.name == edge.toV or state.currentVertex.name == edge.fromV):
            return False  # a state is not legal if the status is unkown and we are at a neighboring vertex
    return True


class State(object):
    def __init__(self, currentVertex: Vertex, BlockagesStatusDict):
        self.currentVertex = currentVertex
        self.blockages = BlockagesStatusDict
        self.graph = Graph()

    def __str__(self):
        s = "STATE\nCurrent vertex: " + str(self.currentVertex) + "{"
        for edge in self.blockages:
            s += "Edge from " + edge.fromV + " to " + edge.toV + ": " + str(self.blockages[edge]) + ", "
        return s + "}\n"

    def getActions(self):
        return self.graph.getConnectedEdges(self.currentVertex)

    def sameStatus(self, other):
        return self.blockages == other.blockages

    def consistentStates(self, otherState):
        for edge, status in self.blockages.items():
            if (status == False or status == True) and otherState.blockages[edge] != status:
                return False
        return True

    def discoveredEdges(self, otherState):
        edges = []
        for blockableEdge in self.blockages.keys():
            if self.blockages[blockableEdge] == UNKNOWN:
                if otherState.blockages[blockableEdge] != UNKNOWN:
                    blockableStat = otherState.blockages[blockableEdge]
                    edges.append((blockableEdge, blockableStat))
        return edges

    def edgesUnknown(self):
        for value in self.blockages.values():
            if value != UNKNOWN:
                return False
        return True

    def goalState(self):
        return self.currentVertex.isGoal
