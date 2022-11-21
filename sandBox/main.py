import os
import csv
import re
import time
import outputStrings as out

NUMBER_PREFIX = '#N'
VERTEX_PREFIX = '#V'
EDGE_PREFIX = '#E'
WEIGHT_PREFIX = 'W'
PEOPLE_PREFIX = 'P'

class Assignment1(object):
    def __init__(self):
        self.graph = None
        self.start_time = time.time()

    def createGraph(self, pathToGraph):
        if os.path.isfile(pathToGraph):
                self.graph = Graph(pathToGraph)
        else:
            print("File given doesn't exist!")
        print("Finished generating graph object")

    def timeConvert(self):
        end_time = time.time()
        sec = end_time - self.start_time
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        return out.TIME.format(int(hours), int(mins), sec)

    def checkValidNumber(self, num, limit):
        validNum = False
        numInt = None
        while not validNum:
            try:
                numInt = int(num)
                if limit > numInt > 0:
                    validNum = True
                else:
                    num = input(out.INVALID_INPUT.format(str(limit)))
            except ValueError:
                num = input(out.INVALID_INPUT.format(str(limit)))
        return numInt

    def numInput(self, text, limit):
        num = input(text)
        return self.checkValidNumber(num, limit)

    def initPosition(self):
        positions = "Choose starting position:\n"
        numOfVert = len(self.graph.vertexes)
        for vertNumber in range(numOfVert):
            positions += str(vertNumber + 1) + ")\t" + str(self.graph.vertexes[vertNumber]) + "\n"
        position = self.numInput(positions, numOfVert + 1)
        return position - 1

    def createAgent1(self, agentType, position):
        if agentType == 1:
            return # Human agent
        elif agentType == 2:
            return # Stupid greedy agent
        elif agentType == 3:
            return # Saboteur agent

    def createAgent2(self, agentType, position):
        if agentType == 1:
            return # Greedy search agent
        elif agentType == 2:
            return # A* search agent
        elif agentType == 3:
            return # Real time A* agent with L expansions

    def firstImpl(self):
        agents = []
        agentString = ["Choose initial position for stupid greedy agent", "Choose initial position for saboteur agent agent"]
        for agent in range(len(agentString)):
            print(agentString[agent])
            position = self.initPosition()
            agents.append(self.createAgent1(agent, position))
        agentType = self.numInput("Choose type for agent number 3:\n"
                                  "1)\tHuman agent\n"
                                  "2)\tStupid greedy agent\n"
                                  "3)\tSaboteur agent\n", 4)
        position = self.initPosition()
        newAgent = self.createAgent1(agentType, position)
        agents.append(newAgent)

    def secondImpl(self):
        numOfAgents = self.numInput("Insert the number of agents - ", 1000)
        agents = []
        for i in range(1, numOfAgents + 1):
            agentType = self.numInput("Choose type for agent number" + str(i) + ":\n"
                                  "1)\tGreedy search agent\n"
                                  "2)\tA* search agent\n"
                                  "3)\tReal time A* agent with L expansions\n", 4)
            position = self.initPosition()
            newAgent = self.createAgent2(agentType, position)
            agents.append(newAgent)

    def userInit(self):
        print('----Welcome to Hurricane Evacuation Problem----')
        implNum = self.numInput("Insert which part to run:\n"
                                "1)\tImplementation part 1\n"
                                "2)\tImplementation part 2\n"
                                "Your choice - ", 3)
        if implNum == 1:
            agents = self.firstImpl()
        else:
            agents = self.secondImpl()

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
                    self.vertexes.append(Vertex(row[0], personCounter, isBrittle))
                elif row[0].startswith(EDGE_PREFIX):
                    self.edges.append(Edge(row[1], row[2], row[3].split(WEIGHT_PREFIX)[1]))


class Vertex(object):
    def __init__(self, name, numberOfPersons:int , isBrittle = False, isBlocked = False):
        self.name = name
        self.persons = numberOfPersons
        self.isBrittle = isBrittle
        self.isBlocked = isBlocked

    def __str__(self):
        return self.name

class Edge(object):
    def __init__(self, fromV, toV, weight):
        self.fromV = fromV
        self.toV = toV
        self.weight = weight


if __name__ == '__main__':
    ass1 = Assignment1()
    ass1.createGraph(os.path.join(os.getcwd(), 'graph.csv'))
    ass1.userInit()
    # program

