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
        self.toSave = []
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
                        self.toSave.append(vertex)
                    self.vertexes.append(vertex)
                elif row[0].startswith(EDGE_PREFIX):
                    self.edges.append(Edge(row[1], row[2], row[3].split(WEIGHT_PREFIX)[1]))

    def getAllBrittle(self):
        return self.brittles

    def getAllToSave(self):
        return self.toSave

    def getVertexByName(self, name):
        for vertex in self.vertexes:
            if vertex.name is name:
                return vertex
        return None
