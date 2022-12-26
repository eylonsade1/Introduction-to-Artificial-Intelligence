import copy

from Graph import Graph


class State(object):
    def __init__(self, maxLocation, minLocation, vertexWithPeopleToSave, brokenVertexes):
        self.toSave = vertexWithPeopleToSave
        self.graph = Graph()
        # todo - reachable for who? + need tpo change all of current location usage
        # self.reachable = utils.getReachableToSave(currentVertex)
        self.brokenVertexes = brokenVertexes
        self.minScore = 0
        self.maxScore = 0
        self.maxLocation = maxLocation
        self.minLocation = minLocation


    def __str__(self):
        return "Current position: {} in the environment: \n{}\n".format(self.currentVertexstr, (self.graph))

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

    def getMaxCurrentLocation(self):
        return self.maxLocation

    def getMinCurrentLocation(self):
        return self.minLocation

    def getAllReachable(self):
        return self.reachable

    def getAllBrokenVertexes(self):
        return self.brokenVertexes

    def getMaxLocation(self):
        return self.maxLocation

    def getMinLocation(self):
        return self.minLocation

    def getMaxScore(self):
        return self.maxScore

    def getMinScore(self):
        return self.minScore

    def successor(self, type_of_agent: str, graph: Graph):
        if type_of_agent == 1: # Max
            return self.maxSuccessor(graph)
        else: # Min
            return self.minSuccessor(graph)
        
    def maxSuccessor(self, graph):
        newStates = []
        for neighbour in graph.getNeighborsListNoWeight(self.maxLocation):
            maxNewScore = self.maxScore
            newState = copy.deepcopy(self)
            # newState.simulated_movements += 1
            if not newState.toSave[neighbour]:
                maxNewScore = self.maxScore + neighbour.numOfPeople()
                newState.saveVertex(neighbour)
            newState.maxScore = maxNewScore
            newStates.append(newState)
        return newStates

    def minSuccessor(self, graph):
        newStates = []
        for neighbour in graph.getNeighborsList(self.minLocation):
            minNewScore = self.minScore
            newState = copy.deepcopy(self)
            # newState.simulated_movements += 1
            if not newState.toSave[neighbour]:
                minNewScore = self.minScore + neighbour.numOfPeople
                newState.saveVertex(neighbour)
            newState.minScore = minNewScore
            newStates.append(newState)
        return newStates
