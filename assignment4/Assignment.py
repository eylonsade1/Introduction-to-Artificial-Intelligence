from Graph import Graph
from Graph import DEFAULT_ROUTE
from State import *
from copy import copy


class Assignment(object):
    def __init__(self, states):
        self.graph = Graph()
        self.states = states
        self.policyPrevious = {}
        self.policyNext = {}
        self.generateArbirtaryInitialation()

    def generateArbirtaryInitialation(self):
        for state in self.states:
            if state.currentVertex.isGoal:
                self.policyPrevious[state] = (0, GOAL)
                self.policyNext[state] = (0, GOAL)
            else:
                self.policyPrevious[state] = (DEFAULT_ROUTE, None)
                self.policyNext[state] = (DEFAULT_ROUTE, None)

    def generatePolicy(self, policy):
        for state in self.states:
            if state.currentVertex.isGoal:
                policy[state] = (0, GOAL)
            else:
                policy[state] = (DEFAULT_ROUTE, None)

    def getStatesExcludingGoal(self):
        relevantStates = []
        for state in self.states:
            if not state.currentVertex.isGoal:
                relevantStates.append(state)
        return relevantStates

    def verifyLegalMove(self, edgeMove, state):
        for edge, blockage in state.blockages.items():
            if edge == edgeMove and blockage is True:
                return False
        return True

    def valueIteration(self):
        changeInPolicy = True
        statesExculdingGoals = self.getStatesExcludingGoal()
        while changeInPolicy:
            changeInPolicy = False
            for state in statesExculdingGoals:
                currVertex = state.currentVertex
                expectedValue = DEFAULT_ROUTE
                for possibleEdgeMove in state.getActions():
                    if not self.verifyLegalMove(possibleEdgeMove, state):
                        continue
                    expectedValueEdge = 0
                    for neighboringState in self.states:
                        edge = self.graph.getEdgeFromVertexes(currVertex, neighboringState.currentVertex)
                        if edge == possibleEdgeMove:
                            prob = self.transition(state, neighboringState)
                            expectedValueEdge += prob*(-int(edge.weight) + self.policyPrevious[neighboringState][0])
                    if expectedValueEdge > expectedValue:
                        expectedValue = expectedValueEdge
                        bestAction = possibleEdgeMove
                if expectedValue > self.policyPrevious[state][0]:
                    changeInPolicy = True
                    self.policyNext[state] = round(expectedValue, 2), bestAction
            self.policyPrevious = copy(self.policyNext)

    def getPolicies(self):
        return self.policyNext

    def sameEdge(self,e1, e2):
        return (e1.fromV == e2.fromV and e1.toV == e2.toV) or (e1.toV == e2.fromV and e1.fromV == e2.toV)


    def transition(self, s1, s2):
        sourceVertex = s1.currentVertex
        destinationVertex = s2.currentVertex
        possiblyBlocked = self.graph.getAllBlockableEdgesFromVertex(destinationVertex)
        if s1.sameStatus(s2):
            for maybeBlockedEdge in possiblyBlocked:
                if s2.blockages[maybeBlockedEdge] == UNKNOWN:
                    return 0
            return 1
        if not s1.consistentStates(s2):
            return 0
        for maybeBlockedEdge in s1.blockages.keys():
            if s1.blockages[maybeBlockedEdge] == UNKNOWN and s2.blockages[maybeBlockedEdge] != UNKNOWN:
                if maybeBlockedEdge not in possiblyBlocked:
                    return 0
            elif s1.blockages[maybeBlockedEdge] == UNKNOWN and s2.blockages[maybeBlockedEdge] == UNKNOWN:
                if maybeBlockedEdge in possiblyBlocked:
                    return 0
        newEdges = s1.discoveredEdges(s2)
        prob = 1
        for edge in newEdges:
            if edge[1] == 1:
                prob *= edge[0].blockageProbability
            else:
                prob *= (1 - edge[0].blockageProbability)
        return round(prob, 2)

    def printNextPolicy(self):
        for poicy in self.policyNext.items():
            state = poicy[0]
            utility = poicy[1][0]
            action = poicy[1][1]
            print(state, "UTILITY:", utility, "\nACTION: ", action, sep="", end="\n\n")

    def findState(self, toVertex, blockageStatus):
        for state in self.states:
            if state.currentVertex.name == toVertex and state.blockages == blockageStatus:
                return state

    def getStartState(self, start):
        for state in self.states:
            if state.currentVertex == start and state.edgesUnknown():
                return state

    def findGoal(self, blockableStatus):
        policies = self.policyNext
        startVertex = self.graph.getStartVertex()
        currentState = self.getStartState(startVertex)
        while not currentState.goalState():
            bestMove = policies[currentState][1]
            print(bestMove)
            edgeStatus = copy(currentState.blockages)
            goalVertex = bestMove.getNewLocation(currentState.currentVertex.name)
            blockableFromGoal = self.graph.getAllBlockableEdgesFromVertex(goalVertex)
            for blockableEdge in blockableFromGoal:
                if blockableStatus[blockableEdge]:
                    edgeStatus[blockableEdge] = True
                else:
                    edgeStatus[blockableEdge] = False
            currentState = self.findState(goalVertex, edgeStatus)
