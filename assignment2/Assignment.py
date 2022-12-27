from Graph import Graph
import time
import OutputStrings as out
from Agent import Agent
from utils import Enum
from games import UtilityFuncs

AGENT_TYPES = Enum(['MaxAgent',
                    'MinAgent'])
class Assignment2(object):
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

    def initPosition(self, agentNumString = "first"):
        positions = "Choose starting position {} agent:\n".format(agentNumString)
        numOfVert = len(self.graph.vertexes)
        for vertNumber in range(numOfVert):
            positions += str(vertNumber + 1) + ")\t" + str(self.graph.vertexes[vertNumber]) + "\n"
        position = self.numInput(positions, numOfVert + 1)
        return position - 1

    def allAgentTerminated(self):
        for agent in self.agents:
            if not agent.terminated:
                return False
        return True

    def initAgents(self, startPositionMax, startPositionMin, impNum):
        if impNum == 1:
            maxAgent = Agent(startPositionMax, AGENT_TYPES.MaxAgent, startPositionMax, doPrune=True)
            minAgent = Agent(startPositionMin, AGENT_TYPES.MinAgent, startPositionMin, doPrune=True)
        elif impNum == 2:
            maxAgent = Agent(startPositionMax, AGENT_TYPES.MaxAgent, startPositionMin,
                             utilityFunction=UtilityFuncs.maxSemiCooperative)
            minAgent = Agent(startPositionMin, AGENT_TYPES.MinAgent, startPositionMax,
                             utilityFunction=UtilityFuncs.minSemiCooperative)
        else:
            maxAgent = Agent(startPositionMax, AGENT_TYPES.MaxAgent, startPositionMin,
                             utilityFunction=UtilityFuncs.fullyCooperative)
            minAgent = Agent(startPositionMin, AGENT_TYPES.MinAgent, startPositionMax,
                             utilityFunction=UtilityFuncs.fullyCooperative)

        maxAgent.otherAgent = minAgent
        minAgent.otherAgent = maxAgent
        self.agents.extend([maxAgent, minAgent])

    def userInit(self):
        print(out.WELCOME_HURRICANE)
        self.agents = []
        impNum = self.numInput(out.CHOOSE_GAME_TYPE)
        startingMax = self.initPosition("first")
        startingMin = self.initPosition("second")
        startingMax = self.graph.getVertexByName(startingMax)
        startingMin = self.graph.getVertexByName(startingMin)

        self.initAgents(startingMax, startingMin, impNum)

    def runAgents(self):
        othersLocation = self.agents[1]
        while not self.allAgentTerminated():
            for agent in self.agents:
                if not agent.terminated:
                    agent.setOthersLocation(othersLocation)
                    agent.act()
                    othersLocation = agent.state.getCurrentLocation()



    def heauristicFunction(self, wrapper):
        return


    def printAgentsState(self):
        for agent in self.agents:
            print(agent)

