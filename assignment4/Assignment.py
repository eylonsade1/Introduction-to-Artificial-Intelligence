from Graph import Graph
from Graph import DEFAULT_ROUTE
from State import GOAL
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
                        if self.graph.getEdgeFromVertexes(currVertex, neighboringState.currentVertex) == possibleEdgeMove:
                            #todo - add transition ,bascially copy their code!!
                            print("Reached transition calculation")
                    if expectedValueEdge < expectedValue:
                        expectedValue = expectedValueEdge
                        bestAction = possibleEdgeMove
                if expectedValue < self.policyPrevious[state][0]:
                    changeInPolicy = True
                    self.policyNext[state] = round(expectedValue, 2), bestAction
            self.policyPrevious = copy(self.policyNext)

    def getPolicies(self):
        return self.policyNext



