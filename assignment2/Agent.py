from collections import defaultdict
import Vertex
from Graph import Graph
from State import State
from utils import *
from games import *
import copy

TIME_LIMIT = 400

class Agent(object):
    def __init__(self, startingPositionMax, startingPositionMin, agentType, utilityFunction=None, doPrune=False):
        self.graph = Graph()
        #todo - add handling of new state structure
        self.state = None #State(self.graph.vertexes[startingPosition], self.graph.getAllToSave())
        self.actionSequence = [startingPositionMax, 0, startingPositionMax]
        self.type = agentType
        self.utilityFunction = utilityFunction
        self.prune = doPrune
        self.movementAmount = 0
        self.timeSpent = 0
        self.individualScore = 0
        self.totalScore = 0 # total score is dependent on game mode
        self.otherAgent = None
        self.terminated = False
        self.states = []
        self.currentPosition = None

    def __str__(self):
        agentString = "---------------\n" \
                      "{}\n" \
                      "people saved: {}\n" \
                      "time spent (weight of edges): {}\n" \
                      "score(total) {}\n" \
                      "---------------\n".format(type(self).__name__, self.individualScore,
                                                 self.timeSpent, self.totalScore)
        return agentString

    def doNoOp(self):
        print("No-Op")

    # todo :prob dont need - added for merge
    def setOthersLocation(self, othersLocation):
        self.othersLocation = othersLocation

    def shouldTerminateGame(self):
        if self.graph.areAllSaved():
            return True
        for state in self.states:
            if equalStates(state, self.state):
                return True

    def strFromSequence(self):
        sequenceString = "["
        for vertex in self.actionSequence:
            sequenceString += str(vertex)
        sequenceString += "]"
        return sequenceString

    def translateSequenceToString(self, actionSequence):
        s = "[ "
        for vertex in actionSequence:
            s += str(vertex) + ", "
        last_index_of_comma = s.rfind(",")
        if last_index_of_comma != -1:
            s = s[:last_index_of_comma] + s[last_index_of_comma + 1:]
        return s + "]"


    def miniMax(self, state: State):
        return []

    def minimaxAlphaBeta(self, state: State):
        return []

    def update_state(self):
        pass

    def act(self):
        print("------ {} ------".format(type(self).__name__))
        self.terminated = self.shouldTerminateGame()
        if not self.terminated:
            if self.movementAmount >= TIME_LIMIT:
                self.terminated = True
                print("TERMINATED\n")
            else:
                self.updateState()
                print("MINIMAXING")
                if self.prune:
                    self.actionSequence = self.minimaxAlphaBeta(self.state)
                else:
                    self.actionSequence = self.miniMax(self.state)
                #todo dependent on the actionSequence returned from state behavior
                self.actionSequence.append(self.actionSequence[2])
                self.move()
        else:
            print("TERMINATED\n")

    def move(self):
        self.movementAmount += 1
        next_vertex = self.actionSequence[0]
        print("Current Vertex: " + str(self.currentPosition))
        print("Moving to: " + str(next_vertex))
        if next_vertex != self.state.currentVertex:
            self.saveVertexOnMove()
        if self.currentPosition.isBrittle:
            self.graph.deleteVertex(self.currentPosition)
        # self.state.currentVertex = next_vertex
        self.timeSpent += 1
        self.actionSequence = self.actionSequence[1:]
        if len(self.actionSequence) == 0:
            self.saveVertexOnMove()
        self.currentPosition = next_vertex

        #todo add termination based on the state
        # if self.reachedGoal(self.state) or self.impossibleToReachGoal(self.state):
        #     self.terminated = True


    #todo fix for current state behavior
    def saveVertexOnMove(self):

        # currentVertex = self.graph.getVertexByName(self.state.currentVertex.name)
        currentVertex = self.currentPosition
        if currentVertex is not None and currentVertex.persons > 0:
            print("Saving: " + str(self.state.currentVertex))
            self.individualScore += currentVertex.persons
            #todo add reprentation of people on state
            # self.state.currentVertex.persons = 0
            currentVertex.persons = 0
        self.state.saveVertex()


    #@todo add state update method - based on relevant state behavior - state recieves
    def updateState(self):
        print("Not yet implemented")

    def maxVal_alphaBeta(self, state: State, plys, alpha, beta):
        if state.shouldTerminateSearch(plys):
            return state.evaluate_alpha_beta()
        v = float('-inf')
        for next_state in state.successor("MAX"):
            v = max(v, self.minVal_alphaBeta(next_state, plys + 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def minVal_alphaBeta(self, state: State, plys, alpha, beta):
        if state.shouldTerminateSearch(plys):
            return state.evaluate_alpha_beta()
        v = float('inf')
        for next_state in state.successor("MIN"):
            v = min(v, self.maxVal_alphaBeta(next_state, plys + 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

class maxAgent(Agent):
    def __init__(self, startingPositionMax, startingPositionMin, agentType, utilityFunction=None, doPrune=False):
        super(maxAgent, self).__init__(startingPositionMax, startingPositionMin,agentType, utilityFunction, doPrune)
        self.currentPosition = startingPositionMax

    def updateState(self):
        graphState = self.graph.getAllToSave()
        self.state.brokenVertexes = self.graph.getAllBroken()
        for vertex in graphState:
            if graphState[vertex]:
                self.state.toSave[vertex] = True
            else:
                self.state.toSave[vertex] = False
        self.state.minLocation = self.otherAgent.state.minLocation
        self.state.maxScore = self.individualScore
        self.state.minScore = self.otherAgent.individualScore

    def maxVal(self, state: State, plys):
        if state.shouldTerminateSearch(plys):
            return state.evaluate()
        bestVal = None
        for neighborState in state.successor("MAX"):
            neighborStateMinVal = self.minVal(neighborState, plys + 1)
            if bestVal is None:
                bestVal = neighborStateMinVal
            bestVal = self.utilityFunction(bestVal, neighborStateMinVal)
        return bestVal

    def minVal(self, state: State, plys):
        if state.shouldTerminateSearch(plys):
            return state.evaluate()
        bestVal = None
        for neighborState in state.successor("MIN"):
            neighborStateMaxVal = self.maxVal(neighborState, plys + 1)
            if bestVal is None:
                bestVal = neighborStateMaxVal
            bestVal = self.otherAgent.utilityFunction(bestVal, neighborStateMaxVal)
        return bestVal

    def miniMax(self, state: State):
        bestVal = None
        goalVertexBestMove = None
        plys = 0
        for neighborState in state.successor("MAX"):
            neighborStateValue = self.minVal(neighborState, plys + 1)
            nextVertex = neighborState.maxLocation
            if bestVal is None:
                bestVal = neighborStateValue
                goalVertexBestMove = nextVertex
            elif not (bestVal == self.utilityFunction(bestVal, neighborStateValue)):
                bestVal = neighborStateValue
                goalVertexBestMove = nextVertex
        return goalVertexBestMove

    def minimaxAlphaBeta(self, state: State):
        goalVertexBestMove = None
        plys = 0
        bestVal = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for neighborState in state.successor("MAX"):
            neighborStateValue = self.minVal_alphaBeta(neighborState, plys + 1, alpha, beta)
            nextVertex = neighborState.maxLocation
            if bestVal < neighborStateValue:
                bestVal = neighborStateValue
                goalVertexBestMove = nextVertex
            alpha = max(bestVal, alpha)
        return goalVertexBestMove


class MinAgent(Agent):
    def __init__(self, startingPositionMax, startingPositionMin, agentType, utilityFunction=None, doPrune=False):
        super(MinAgent, self).__init__(startingPositionMax, startingPositionMin, agentType, utilityFunction, doPrune)
        self.currentPosition = startingPositionMin

    def updateState(self):
        graphState = self.graph.getAllToSave()
        self.state.maxLocation = self.otherAgent.state.maxLocation
        self.state.brokenVertexes = self.graph.getAllBroken()
        for vertex in graphState:
            if graphState[vertex]:
                self.state.toSave[vertex] = True
            else:
                self.state.toSave[vertex] = False
        self.state.maxScore = self.otherAgent.individualScore
        self.state.minScore = self.individualScore
        return

    def maxVal(self, state: State, plys):
        if state.shouldTerminateSearch(plys):
            return state.evaluate()
        bestVal = None
        for neighborState in state.successor("MAX"):
            neighborStateMinVal = self.minVal(neighborState, plys + 1)
            if bestVal is None:
                bestVal = neighborStateMinVal
            bestVal = self.otherAgent.utilityFunction(bestVal, neighborStateMinVal)
        return bestVal

    def minVal(self, state: State, plys):
        if state.shouldTerminateSearch(plys):
            return state.evaluate()
        bestVal = None
        for neighborState in state.successor("MIN"):
            neighborStateMaxVal = self.maxVal(neighborState, plys + 1)
            if bestVal is None:
                bestVal = neighborStateMaxVal
            bestVal = self.utilityFunction(bestVal, neighborStateMaxVal)
        return bestVal

    def miniMax(self, state: State):
        bestVal = None
        goalVertexBestMove = None
        plys = 0
        for neighborState in state.successor("MIN"):
            neighborStateValue = self.maxVal(neighborState, plys + 1)
            goalVertex = neighborState.minLocation
            if bestVal is None:
                bestVal = neighborStateValue
                goalVertexBestMove = goalVertex
            elif not (bestVal == self.utilityFunction(bestVal, neighborStateValue)):
                bestVal = neighborStateValue
                goalVertexBestMove = goalVertex
        return goalVertexBestMove

    def minimaxAlphaBeta(self, state: State):
        goalVertexBestMove = None
        plys = 0
        bestVal = float('inf')
        alpha = float('-inf')
        beta = float('inf')
        for neighborState in state.successor("MIN"):
            neighborStateValue = self.maxVal_alphaBeta(neighborState, plys + 1, alpha, beta)
            goalVertex = neighborState.minLocation
            if bestVal > neighborStateValue:
                bestVal = neighborStateValue
                goalVertexBestMove = goalVertex
            beta = min(bestVal, beta)
        return goalVertexBestMove