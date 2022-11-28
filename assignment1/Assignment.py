from Graph import Graph
import time
import OutputStrings as out
import Agent
import utils

class Assignment1(object):
    def __init__(self):
        self.graph = Graph()
        self.start_time = time.time()
        self.agents = []

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

    def getDepth(self):
        valid = False
        userVal = 0
        while not valid:
            userVal = input("Choose A-Star depth limit")
            if userVal > 0:
                valid = True
            else:
                print("We wish our AI could perform moves looking at negative amount of moves\n"
                      "choose a positive number")
        return userVal

    def allAgentTerminated(self):
        for agent in self.agents:
            if not agent.terminated:
                return False
        return True

    def createAgent1(self, agentType, position):
        if agentType == 1:
            return Agent.HumanAgent(position)
        elif agentType == 2:
            return Agent.StupidGreedy(position)
        elif agentType == 3:
            return Agent.Saboteur(position)

    def createAgent2(self, agentType, position):
        if agentType == 1:
            return Agent.greedyAgent(self.heauristicFunction, position)
        elif agentType == 2:
            return Agent.AStarAgent(self.heauristicFunction, position)
        elif agentType == 3:
            depth = self.getDepth()
            return Agent.AStarAgentDepth(self.heauristicFunction, position, depth)

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
        return agents

    def secondImpl(self):
        numOfAgents = self.numInput(out.CHOOSE_NUM_OF_AGENTS, 1000)
        agents = []
        for i in range(1, numOfAgents + 1):
            agentType = self.numInput(out.CHOOSE_AGENT_PART2.format(str(i)), 4)
            position = self.initPosition()
            newAgent = self.createAgent2(agentType, position)
            agents.append(newAgent)
        return agents

    def userInit(self):
        print(out.WELCOME_HURRICANE)
        implNum = self.numInput(out.CHOOSE_ASS_PART, 3)
        if implNum == 1:
            self.agents = self.firstImpl()
        else:
            self.agents = self.secondImpl()

    def runAgents(self):
        while not self.allAgentTerminated():
            for agent in self.agents:
                if not agent.terminated:
                    agent.act()

        for agent in self.agents:
            print(agent)

    def heauristicFunction(self, wrapper):
        currentPos = wrapper.state.currentVertex.name
        s = utils.spanning_trees(Graph(), currentPos)
        minWeight = utils.minTree(s, currentPos, wrapper.state)
        return minWeight

    def printAgentsState(self):
        for agent in self.agents:
            print(agent)


