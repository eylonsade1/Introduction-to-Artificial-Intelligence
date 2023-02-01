import csv
from Edge import Edge
from Vertex import Vertex
from Singleton import Singleton

NUMBER_PREFIX = '#V'
EDGE_PREFIX = '#E'
BRITTLE_PREFIX = '#B'
WEIGHT_PREFIX = 'W'
START_PREFIX = '#Start'
TARGET_PREFIX = '#Target'
VERTEX_NAME_PREFIX = "#V"
PROBABILITY = "p"
START = "s"
GOAL = "g"
DEFAULT_ROUTE = 10000

class Graph(Singleton):
    def __init__(self):
        self.vertexes = []
        self.edges = []
        self.broken = []
        self.adjMatrix = None

    def __str__(self):
        graphPrint = "Edges :\n ------------------ \n"
        for edge in self.edges:
            graphPrint += str(edge)
        graphPrint += "Vertexes :\n ------------------ \n"
        for vertex in self.vertexes:
            graphPrint += str(vertex)
        return graphPrint

    def makeVertexes(self, amountOfVertexes):
        for vertexNumber in range(amountOfVertexes):
            self.vertexes.append(Vertex(VERTEX_NAME_PREFIX + str(vertexNumber + 1)))

    def readCsvFillInfo(self, csvFilePath):
        with open(csvFilePath, newline='') as graophFileCsv:
            spamreader = csv.reader(graophFileCsv, delimiter=',')
            for row in spamreader:
                if row[0] == NUMBER_PREFIX:
                    self.makeVertexes(int(row[1]))
                elif row[0].startswith(BRITTLE_PREFIX):
                    self.updateVertex(row[1], row[2], PROBABILITY)
                elif row[0].startswith(EDGE_PREFIX):
                    self.edges.append(
                        Edge(self.getVertexByName(VERTEX_NAME_PREFIX + row[1]), self.getVertexByName(VERTEX_NAME_PREFIX + row[2]), row[3].split(WEIGHT_PREFIX)[1]))
                elif row[0].startswith(START_PREFIX):
                    self.updateVertex(row[1], True, START)
                elif row[0].startswith(TARGET_PREFIX):
                    self.updateVertex(row[1], True, GOAL)
        self.edges.append(
            Edge(self.getStartVertex(), self.getGoalVertex(), DEFAULT_ROUTE)
        )

    def getStartVertex(self):
        for vertex in self.vertexes:
            if vertex.isStart:
                return vertex

    def getGoalVertex(self):
        for vertex in self.vertexes:
            if vertex.isGoal:
                return vertex

    def updateVertex(self, vertexNumber, toUpdate, field):
        vertex: Vertex = self.getVertexByName(VERTEX_NAME_PREFIX + str(vertexNumber))
        if vertex:
            if field == PROBABILITY:
                vertex.setBrokenProb(toUpdate)
            elif field == START:
                vertex.setIsStart(toUpdate)
            elif field == GOAL:
                vertex.setIsGoal(toUpdate)
        else:
            print("During update field {} the vertex {} given does not exist".format(field, vertexNumber))

    def checkIfBrittle(self, name):
        vertex = self.getVertexByName(name)
        return vertex.isBrittle

    def getVertexByName(self, name):
        for vertex in self.vertexes:
            if vertex.name == name:
                return vertex
        return None

    def buildMatrix(self):
        self.adjMatrix = [[0 for x in self.vertexes] for x in self.vertexes]
        for edge in self.edges:
            aCoordinate = int(edge.toV.split(VERTEX_NAME_PREFIX)[1]) - 1
            bCoordinate = int(edge.fromV.split(VERTEX_NAME_PREFIX)[1]) - 1
            self.adjMatrix[aCoordinate][bCoordinate] = int(edge.weight)
            self.adjMatrix[bCoordinate][aCoordinate] = int(edge.weight)

    def getEdgeWeigtFromVerName(self, vertexFrom, vertexTo):
        for edge in self.edges:
            if (edge.fromV == vertexFrom and edge.toV == vertexTo) or (
                    edge.fromV == vertexTo and edge.toV == vertexFrom):
                return int(edge.weight)
        return 0

    def getNeighborsList(self, vertex: Vertex):
        neighbors = []
        for edge in self.edges:
            if edge.fromV == vertex.name:
                weight = self.getEdgeWeigtFromVerName(vertex.name, edge.toV)
                neighbors.append(tuple((self.getVertexByName(edge.toV), int(weight))))
            elif edge.toV == vertex.name:
                weight = self.getEdgeWeigtFromVerName(edge.fromV, vertex.name)
                neighbors.append(tuple((self.getVertexByName(edge.fromV), int(weight))))
        return neighbors

    def getConnectedEdges(self, vertex):
        connectedEdges = []
        for edge in self.edges:
            if edge.fromV == vertex.name:
                connectedEdges.append(edge)
            elif edge.toV == vertex.name:
                connectedEdges.append(edge)
        return connectedEdges

    def getVertexNumber(self, vertex: Vertex):
        for vertexNumber in range(len(self.vertexes)):
            if self.vertexes[vertexNumber] == vertex:
                return vertexNumber

    def getAllBlockableEdges(self):
        allEdgesList = []
        for vertex in self.vertexes:
            if vertex.brokenProb:
                for edge in self.getConnectedEdges(vertex):
                    if edge not in allEdgesList:
                        allEdgesList.append(edge)
        return allEdgesList

