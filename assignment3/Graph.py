import csv
from Edge import Edge
from Vertex import Vertex
from Weather import Weather
from Singleton import Singleton

NUMBER_PREFIX = '#N'
VERTEX_PREFIX = '#V'
EDGE_PREFIX = '#E'
WEIGHT_PREFIX = 'W'
WEATHER_PREFIX = '#W'
BLOCKAGE_PROBABILITY_PREFIX = 'F'
P1_PREFIX = "#P1"
P2_PREFIX = "#P2"

class Graph(Singleton):
    def __init__(self):
        self.numOfPoints = None
        self.vertexes = []
        self.edges = []
        self.broken = []
        self.weather = None
        self.adjMatrix = None
        self.p1 = 0
        self.p2 = 0

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
                    mildBlockageProbability = 0
                    for field in row:
                        if field.startswith(BLOCKAGE_PROBABILITY_PREFIX):
                            mildBlockageProbability = field.split(BLOCKAGE_PROBABILITY_PREFIX)[1]
                            mildBlockageProbability = float(mildBlockageProbability)

                    vertex = Vertex(row[0], mildBlockageProbability)
                    self.vertexes.append(vertex)
                elif row[0].startswith(EDGE_PREFIX):
                    self.edges.append(Edge(VERTEX_PREFIX + row[1],VERTEX_PREFIX + row[2], row[3].split(WEIGHT_PREFIX)[1], row[0]))

                elif row[0].startswith(WEATHER_PREFIX):
                    self.weather = Weather(float(row[1]), float(row[2]), float(row[3]))

                elif row[0].startswith(P1_PREFIX):
                    self.p1 = float(row[1])

                elif row[0].startswith(P2_PREFIX):
                    self.p2 = float(row[1])

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

    def get_vertex_list_from_edges(self, edges):
        vertexes = []
        for edge in edges:
            if edge.fromV not in vertexes:
                vertexes.append(edge.fromV)
            if edge.toV not in vertexes:
                vertexes.append(edge.toV)
        return vertexes

    def get_edge_by_name(self, edge):
        for e in self.edges:
            if edge in e.name:
                return e
