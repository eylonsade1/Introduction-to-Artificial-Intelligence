import copy

from utils import *
from copy import *

NUM_OF_PLYS = 10

class State(object):
    def __init__(self, maxLocation, minLocation):
        self.graph = Graph()
        self.toSave = self.graph.getAllToSave()
        self.brokenVertexes = self.graph.getAllBroken()
        self.minScore = 0
        self.maxScore = 0
        self.maxLocation = maxLocation
        self.minLocation = minLocation


    def __str__(self):
        return "---state---- \n" \
               "Location max {} score max {}\n" \
               "Location min {} score min {}\n" \
               "Broken vertexes {}\n" \
               "saved vertexes status {}".format(self.maxLocation, self.maxScore,
                                                 self.minLocation, self.minScore,
                                                 self.brokenVertexes, self.toSave)


    def shouldTerminateSearch(self, numOfPlys):
        if numOfPlys == NUM_OF_PLYS:
            return True
        return self.areAllSaved()

    def updateState(self):
        graphState = self.graph.getAllToSave()
        self.brokenVertexes = self.graph.getAllBroken()
        for vertex in graphState:
            if graphState[vertex]:
                self.toSave[vertex] = True
            else:
                self.toSave[vertex] = False

    def saveVertex(self, location):
        self.toSave[location] = True

    def areAllSaved(self):
        for vertex in self.toSave:
            if not self.toSave[vertex]:
                return False
        return True

    def reachableFromPosition(self):
        return self.reachable

    def setReachableFromVertex(self, reachableList):
        self.reachable = reachableList

    def getAllToSaveByName(self):
        needSave = []
        for key, value in self.toSave.items():
            if not value:
                needSave.append(key.name)
        return needSave

    def getAllReachable(self):
        return self.reachable

    def getAllBrokenVertexes(self):
        return self.brokenVertexes

    def getMaxLocation(self):
        return self.maxLocation

    def getMinLocation(self):
        return self.minLocation

    def successor(self, type_of_agent: str):
        if type_of_agent == 1: # Max
            return self.maxSuccessor()
        else: # Min
            return self.minSuccessor()
        
    def maxSuccessor(self):
        newStates = []
        for neighbour in self.graph.getNeighborsListNoWeight(self.maxLocation):
            if neighbour in self.brokenVertexes:
                continue
            maxNewScore = self.maxScore
            newState = copy.deepcopy(self)
            if not newState.toSave[neighbour]:
                maxNewScore = self.maxScore + neighbour.numOfPeople()
                newState.saveVertex(neighbour)
            if neighbour.isBrittle:
                self.brokenVertexes.append(neighbour)
            newState.maxLocation = neighbour
            newState.maxScore = maxNewScore
            newStates.append(newState)
        return newStates

    def minSuccessor(self):
        newStates = []
        for neighbour in self.graph.getNeighborsList(self.minLocation):
            if neighbour in self.brokenVertexes:
                continue
            minNewScore = self.minScore
            newState = copy.deepcopy(self)
            if not newState.toSave[neighbour]:
                minNewScore = self.minScore + neighbour.numOfPeople
                newState.saveVertex(neighbour)
            if neighbour.isBrittle:
                self.brokenVertexes.append(neighbour)
            newState.minLocation = neighbour
            newState.minScore = minNewScore
            newStates.append(newState)
        return newStates

    def evaluate(self):
        return self.maxScore, self.minScore

    def evalAlphaBeta(self):
        return self.maxScore - self.minScore

def equalStates(state1: State, state2: State):
    toSave2 = state2.getAllToSaveByName()
    for vertex in state1.getAllToSaveByName():
        if vertex not in toSave2:
            return False

    reachable2 = state2.getAllReachable()
    for vertex in state1.getAllReachable():
        if vertex not in reachable2:
            return False

    broken2 = state2.getAllBrokenVertexes()
    for vertex in state1.getAllBrokenVertexes():
        if vertex not in broken2:
            return False

    if state1.getMinLocation() != state2.getMinLocation():
        return False

    if state1.getMaxLocation() != state2.getMaxLocation():
        return False

    return True