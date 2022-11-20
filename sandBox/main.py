import os
import csv
import re

NUMBER_PREFIX = '#N'
VERTEX_PREFIX = '#V'
EDGE_PREFIX = '#E'
WEIGHT_PREFIX = 'W'
PEOPLE_PREFIX = 'P'

class Assignment1(object):
    def __init__(self):
        self.graph = None
    def createGraph(self, pathToGraph):
        if os.path.isfile(pathToGraph):
                self.graph = Graph(pathToGraph)
        else:
            print("File given doesn't exist!")
        print("Finished generating graph object")

class Graph(object):
    def __init__(self, csvFilePath):
        self.numOfPoints = None
        self.vertexes = []
        self.edges = []
        self.readCsvFillInfo(csvFilePath)
    def readCsvFillInfo(self, csvFilePath):
        with open(csvFilePath, newline='') as graophFileCsv:
            spamreader = csv.reader(graophFileCsv, delimiter=',')
            for row in spamreader:
                if row[0] == NUMBER_PREFIX:
                    self.numOfPoints = row[1]
                elif row[0].startswith(VERTEX_PREFIX):
                    personCounter = 0
                    isBrittle = False
                    for field in row:
                        if field.startswith(PEOPLE_PREFIX):
                            personCounter = field.split(PEOPLE_PREFIX)[1]
                        elif field == 'B':
                            isBrittle = True
                    self.vertexes.append(Vertex(row[0], personCounter, isBrittle ))
                elif row[0].startswith(EDGE_PREFIX):
                    self.edges.append(Edge(row[1], row[2], row[3].split(WEIGHT_PREFIX)[1]))

class Vertex(object):
    def __init__(self, name, numberOfPersons:int , isBrittle = False):
        self.name = name
        self.persons = numberOfPersons
        self.isBrittle = isBrittle

class Edge(object):
    def __init__(self, fromV, toV, weight):
        self.fromV = fromV
        self.toV = toV
        self.weight = weight


if __name__ == '__main__':
    ass1 = Assignment1()
    ass1.createGraph(os.path.join(os.getcwd(), 'graph.csv'))
