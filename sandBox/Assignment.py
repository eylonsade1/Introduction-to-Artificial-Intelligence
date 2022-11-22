from Graph import Graph
import time
import os
import OutputStrings as out
import Agent

class Assignment1(object):
    def __init__(self):
        self.graph = None
        self.start_time = time.time()

    def createGraph(self, pathToGraph):
        if os.path.isfile(pathToGraph):
            self.graph = Graph(pathToGraph)
        else:
            print(out.FILE_DOESNT_EXIST)
        print(out.GRAPH_FINISHED)

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
        agentString = out.POSITION_PART1
        for agent in range(len(agentString)):
            print(agentString[agent])
            position = self.initPosition()
            agents.append(self.createAgent1(agent, position))
        agentType = self.numInput(out.CHOOSE_AGENT3, 4)
        position = self.initPosition()
        newAgent = self.createAgent1(agentType, position)
        agents.append(newAgent)

    def secondImpl(self):
        numOfAgents = self.numInput(out.CHOOSE_NUM_OF_AGENTS, 1000)
        agents = []
        for i in range(1, numOfAgents + 1):
            agentType = self.numInput(out.CHOOSE_AGENT_PART2.format(str(i)), 4)
            position = self.initPosition()
            newAgent = self.createAgent2(agentType, position)
            agents.append(newAgent)

    def userInit(self):
        print(out.WELCOME_HURRICANE)
        implNum = self.numInput(out.CHOOSE_ASS_PART, 3)
        if implNum == 1:
            agents = self.firstImpl()
        else:
            agents = self.secondImpl()
