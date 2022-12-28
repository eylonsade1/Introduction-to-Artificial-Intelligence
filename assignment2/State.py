import copy

from utils import *

NUM_OF_PLYS = 10

class State(object):
    def __init__(self, maxLocation, minLocation):
        self.graph = Graph()
        self.brokenVertexes = []
        self.toSave = dict()
        self.updateState()
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
        self.brokenVertexes = copy.copy(self.graph.getAllBroken())
        for vertex in graphState:
            if graphState[vertex]:
                self.toSave[vertex] = True
            else:
                self.toSave[vertex] = False

    def shallowCopy(self):
        newBroken = []
        for vertex in self.brokenVertexes:
            newBroken.append(vertex)
        self.brokenVertexes = newBroken

        newToSave = dict()
        for vertex, val in self.toSave.items():
            newToSave[vertex] = val
        self.toSave = newToSave

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
        if type_of_agent == "MAX": # Max
            return self.maxSuccessor()
        else: # Min
            return self.minSuccessor()
        
    def maxSuccessor(self):
        # print("\n\nmin location   ---->    ", self.minLocation)
        # print("maxSuccessor\ncurrent location -->  ", self.maxLocation)
        newStates = []
        neighboursAndMe = self.graph.getNeighborsListNoWeight(self.maxLocation)
        neighboursAndMe.append(self.maxLocation)
        for neighbour in neighboursAndMe:
            if neighbour in self.brokenVertexes:
                continue
            maxNewScore = self.maxScore
            newState = copy.copy(self)
            self.shallowCopy()
            if not newState.toSave[neighbour]:
                maxNewScore += neighbour.numOfPeople()
                newState.saveVertex(neighbour)
            newState.maxLocation = neighbour
            newState.maxScore = maxNewScore
            if self.maxLocation.isBrittle and self.maxLocation != newState.maxLocation:
                newState.brokenVertexes.append(self.maxLocation)
            # if not self.equalStates(newState, self):
            newStates.append(newState)
            # print("vertex added ----->  ", newState.maxLocation, " with score  ==  ", maxNewScore)
        return newStates

    def minSuccessor(self):
        # print("\n\nmax location   ---->    ", self.maxLocation)
        # print("minSuccessor\ncurrent location -->  ", self.minLocation)
        newStates = []
        neighboursAndMe = self.graph.getNeighborsListNoWeight(self.minLocation)
        neighboursAndMe.append(self.minLocation)
        for neighbour in neighboursAndMe:
            if neighbour in self.brokenVertexes:
                continue
            minNewScore = self.minScore
            newState = copy.copy(self)
            self.shallowCopy()
            if not newState.toSave[neighbour]:
                minNewScore += neighbour.numOfPeople()
                newState.saveVertex(neighbour)
            newState.minLocation = neighbour
            newState.minScore = minNewScore
            if self.minLocation.isBrittle and self.minLocation != newState.minLocation:
                newState.brokenVertexes.append(self.minLocation)
            # if not self.equalStates(newState, self):
            newStates.append(newState)
            # print("vertex added ----->  ", newState.minLocation, " with score  ==  ", minNewScore)
        return newStates

    def evaluate(self, plys):
        return self.maxScore, self.minScore, plys

    def evalAlphaBeta(self):
        return self.maxScore - self.minScore

    def equalStates(self, state1, state2):
        toSave2 = state2.getAllToSaveByName()
        for vertex in state1.getAllToSaveByName():
            if vertex not in toSave2:
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
