import csv
from Edge import Edge
from Vertex import Vertex
from Singleton import Singleton

NUMBER_PREFIX = '#N'
VERTEX_PREFIX = '#V'
EDGE_PREFIX = '#E'
WEIGHT_PREFIX = 'W'
PEOPLE_PREFIX = 'P'


class Graph(Singleton):
    def __init__(self):
        self.numOfPoints = None
        self.vertexes = []
        self.edges = []
        self.brittles = []
        self.toSave = dict()
        self.broken = []
        self.adjMatrix = None

    def __str__(self):
        graphPrint ="Edges :\n ------------------ \n"
        for edge in self.edges:
            graphPrint += str(edge)
        graphPrint += "Vertexes :\n ------------------ \n"
        for vertex in self.vertexes:
            graphPrint += str(vertex)
        return graphPrint

    def readCsvFillInfo(self, csvFilePath):
        with open(csvFilePath, newline='') as graophFileCsv:
            spamreader = csv.reader(graophFileCsv, delimiter=',')
            for row in spamreader:
                if row[0] == NUMBER_PREFIX:
                    self.numOfPoints = row[1]
                elif row[0].startswith(VERTEX_PREFIX):
                    personCounter = 0
                    isBrittle = False
                    peopleToSave = False
                    for field in row:
                        if field.startswith(PEOPLE_PREFIX):
                            personCounter = field.split(PEOPLE_PREFIX)[1]
                            peopleToSave = True
                        elif field == 'B':
                            isBrittle = True

                    vertex = Vertex(row[0], personCounter, isBrittle)
                    if isBrittle:
                        self.brittles.append(vertex)
                    if peopleToSave:
                        self.toSave[vertex] = False
                    # else:
                    #     self.toSave[vertex] = True
                    self.vertexes.append(vertex)
                elif row[0].startswith(EDGE_PREFIX):
                    self.edges.append(Edge(VERTEX_PREFIX + row[1],VERTEX_PREFIX + row[2], row[3].split(WEIGHT_PREFIX)[1]))

    def getAllBrittle(self):
        return self.brittles

    def checkIfBrittle(self, name):
        vertex = self.getVertexByName(name)
        return vertex.isBrittle

    def getAllToSave(self):
        for vertex in self.vertexes:
            if int(vertex.persons) == 0:
                self.toSave[vertex] = True
        return self.toSave

    def getAllLeftToSave(self):
        needSave = []
        for vertex in self.vertexes:
            if int(vertex.persons) > 0:
                needSave.append(vertex)
        return needSave

    def getAllToSaveByName(self):
        leftToSave = []
        for vertex in self.vertexes:
            if int(vertex.persons) > 0:
                leftToSave.append(vertex.name)
        return leftToSave

    def getVertexByName(self, name):
        for vertex in self.vertexes:
            if vertex.name == name:
                return vertex
        return None

    def deleteVertex(self, vertexToDelete: Vertex):
        print("Agent moved from brittle vertex - updating graph")
        for vertex in self.vertexes:
            if vertex == vertexToDelete:
                self.vertexes.remove(vertex)
        for vertex in self.brittles:
            if vertex == vertexToDelete:
                self.brittles.remove(vertex)
        edgesToDelete = []
        for edge in self.edges:
            if edge.fromV == vertexToDelete.name or edge.toV == vertexToDelete.name:
                edgesToDelete.append(edge)

        for toBreak in edgesToDelete:
            self.edges.remove(toBreak)

        self.broken.append(vertexToDelete)

    def buildMatrix(self):
        self.adjMatrix = [[0 for x in self.vertexes] for x in self.vertexes]
        for edge in self.edges:
            aCoordinate = int(edge.toV.split(VERTEX_PREFIX)[1]) -1
            bCoordinate = int(edge.fromV.split(VERTEX_PREFIX)[1]) -1
            self.adjMatrix[aCoordinate][bCoordinate] = int(edge.weight)
            self.adjMatrix[bCoordinate][aCoordinate] = int(edge.weight)

    def getEdgeWeigtFromVerName(self, vertexFrom, vertexTo):
        for edge in self.edges:
            if (edge.fromV == vertexFrom and edge.toV == vertexTo) or (edge.fromV == vertexTo and edge.toV == vertexFrom) :
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

    def getVertexNumber(self, vertex: Vertex):
        for vertexNumber in range(len(self.vertexes)):
            if self.vertexes[vertexNumber] == vertex:
                return vertexNumber
