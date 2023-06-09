from Graph import Graph
import utils


class State(object):
    def __init__(self, currentVertex, vertexWithPeopleToSave):
        self.currentVertex = currentVertex
        self.toSave = vertexWithPeopleToSave
        self.graph = Graph()
        self.reachable = utils.getReachableToSave(currentVertex)

    def __str__(self):
        return "Current position: {} in the environment: \n{}\n".format(self.currentVertexstr, (self.graph))

    def updateState(self):
        graphState = self.graph.getAllToSave()
        for vertex in graphState:
            if graphState[vertex]:
                self.toSave[vertex] = True
            else:
                self.toSave[vertex] = False

    def saveVertex(self):
        self.toSave[self.currentVertex] = True

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
