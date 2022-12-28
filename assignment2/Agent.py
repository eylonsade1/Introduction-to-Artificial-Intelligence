from State import State
from utils import *


TIME_LIMIT = 400
POSITIVE_INFINITE = float('inf')
NEGATIVE_INFINITE = float('-inf')


class Agent(object):
    def __init__(self, startingPositionMax, startingPositionMin, utilityFunction=None, doPrune=False):
        self.graph = Graph()
        self.state = State(startingPositionMax, startingPositionMin)
        self.actionSequence = []
        self.utilityFunction = utilityFunction
        self.prune = doPrune
        self.movementAmount = 0
        self.timeSpent = 0
        self.individualScore = 0
        self.otherAgent = None
        self.terminated = False
        self.states = []
        self.currentPosition = None

    def __str__(self):
        agentString = "---------------\n" \
                      "{}\n" \
                      "people saved: {}\n" \
                      "time spent (weight of edges): {}\n" \
                      "---------------\n".format(type(self).__name__, self.individualScore,
                                                 self.timeSpent)
        return agentString

    def doNoOp(self):
        print("No-Op")

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
                    self.actionSequence.append(self.minimaxAlphaBeta(self.state))
                else:
                    self.actionSequence.append(self.miniMax(self.state))
                self.move()
        else:
            print("TERMINATED\n")

    def move(self):
        self.movementAmount += 1
        next_vertex = self.actionSequence[0]
        print("Current Vertex: " + str(self.currentPosition))
        if not next_vertex is None:
            print("Moving to: " + str(next_vertex))
            if next_vertex != self.currentPosition:
                self.saveVertexOnMove()
            if self.currentPosition.isBrittle:
                self.graph.deleteVertex(self.currentPosition)
            self.timeSpent += 1
            self.actionSequence = self.actionSequence[1:]
            if len(self.actionSequence) == 0:
                self.saveVertexOnMove()
            self.currentPosition = next_vertex
            self.updateStateLocation()
        else:
            self.terminated = True
            print("Agent can not continue, on a broken vertex !")

    def saveVertexOnMove(self):
        currentVertex = self.currentPosition
        if currentVertex is not None and currentVertex.persons > 0:
            print("Saving: " + str(self.currentPosition))
            self.individualScore += currentVertex.persons
            currentVertex.persons = 0
        self.state.saveVertex(self.currentPosition)


    def updateState(self):
        print("Not yet implemented")

    def updateStateLocation(self):
        print("Not yet implemented")

    def maxVal_alphaBeta(self, state: State, plys, alpha, beta):
        if state.shouldTerminateSearch(plys):
            return state.evalAlphaBeta()
        v = NEGATIVE_INFINITE
        neighboringStates = state.successor("MAX")
        for neighborState in neighboringStates:
            v = max(v, self.minVal_alphaBeta(neighborState, plys + 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def minVal_alphaBeta(self, state: State, plys, alpha, beta):
        if state.shouldTerminateSearch(plys):
            return state.evalAlphaBeta()
        v = POSITIVE_INFINITE
        neighboringStates = state.successor("MIN")
        for neighborState in neighboringStates:
            v = min(v, self.maxVal_alphaBeta(neighborState, plys + 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


class MaxAgent(Agent):
    def __init__(self, startingPositionMax, startingPositionMin, utilityFunction=None, doPrune=False):
        super(MaxAgent, self).__init__(startingPositionMax, startingPositionMin, utilityFunction, doPrune)
        self.currentPosition = startingPositionMax
        self.saveVertexOnMove()

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
            return state.evaluate(plys)
        bestVal = None
        for neighborState in state.successor("MAX"):
            neighborStateMinVal = self.minVal(neighborState, plys + 1)
            if bestVal is None:
                bestVal = neighborStateMinVal
            bestVal = self.utilityFunction(bestVal, neighborStateMinVal)
        return bestVal

    def minVal(self, state: State, plys):
        if state.shouldTerminateSearch(plys):
            return state.evaluate(plys)
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
        bestVal = NEGATIVE_INFINITE
        alpha = NEGATIVE_INFINITE
        beta = POSITIVE_INFINITE
        neighboringStates = state.successor("MAX")
        for neighborState in neighboringStates:
            neighborStateValue = self.minVal_alphaBeta(neighborState, plys + 1, alpha, beta)
            nextVertex = neighborState.maxLocation
            if bestVal < neighborStateValue:
                bestVal = neighborStateValue
                goalVertexBestMove = nextVertex
            alpha = max(bestVal, alpha)
        return goalVertexBestMove

    def updateStateLocation(self):
        self.state.maxLocation = self.currentPosition

class MinAgent(Agent):
    def __init__(self, startingPositionMax, startingPositionMin, utilityFunction=None, doPrune=False):
        super(MinAgent, self).__init__(startingPositionMax, startingPositionMin, utilityFunction, doPrune)
        self.currentPosition = startingPositionMin
        self.saveVertexOnMove()

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
            return state.evaluate(plys)
        bestVal = None
        for neighborState in state.successor("MAX"):
            neighborStateMinVal = self.minVal(neighborState, plys + 1)
            if bestVal is None:
                bestVal = neighborStateMinVal
            bestVal = self.otherAgent.utilityFunction(bestVal, neighborStateMinVal)
        return bestVal

    def minVal(self, state: State, plys):
        if state.shouldTerminateSearch(plys):
            return state.evaluate(plys)
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
        bestVal = POSITIVE_INFINITE
        alpha = NEGATIVE_INFINITE
        beta = POSITIVE_INFINITE
        for neighborState in state.successor("MIN"):
            neighborStateValue = self.maxVal_alphaBeta(neighborState, plys + 1, alpha, beta)
            goalVertex = neighborState.minLocation
            if bestVal > neighborStateValue:
                bestVal = neighborStateValue
                goalVertexBestMove = goalVertex
            beta = min(bestVal, beta)
        return goalVertexBestMove

    def updateStateLocation(self):
        self.state.minLocation = self.currentPosition
