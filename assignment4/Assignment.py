from Graph import Graph
from Graph import DEFAULT_ROUTE

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
                self.policyPrevious[state] = (0)
                self.policyNext[state] = (0)
            else:
                self.policyPrevious[state] = (DEFAULT_ROUTE)
                self.policyNext[state] = (DEFAULT_ROUTE)


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
            for state in statesExculdingGoals:
                currVertex = state.currentVertex
                expectedValue = DEFAULT_ROUTE
                for possibleEdgeMove in state.getActions():
                    if not self.verifyLegalMove(possibleEdgeMove, state):
                        continue
                    expectedValueEdge = 0
                    for neighboringState in self.states:
                        if self.graph.getEdgeFromVertexes(currVertex, neighboringState.currentVertex) == possibleEdgeMove:
                            print("Reached transition calculation")
                    if expectedValueEdge < expectedValue:
                        expectedValue = expectedValueEdge
                        bestAction = possibleEdgeMove



