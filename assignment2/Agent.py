from collections import defaultdict
import Vertex
from Graph import Graph
from State import State
from utils import *
import copy

SCORE_MULTIPLYER = 1000
TIME_LIMIT = 400

class Agent(object):
    def __init__(self, startingPosition, agentType, othersLocation, utilityFunction=None, doPrune=False):
        self.graph = Graph()
        self.state = State(self.graph.vertexes[startingPosition], self.graph.getAllToSave(), self.graph.getAllBroken(), othersLocation)
        self.actionSequence = [startingPosition, 0, startingPosition]
        self.type = agentType
        self.utilityFunction = utilityFunction
        self.prune = doPrune
        self.movementAmount = 0
        self.amountOfPeopleSaved = 0
        self.timeSpent = 0
        self.score = 0
        self.otherAgent = None
        self.terminated = False
        self.othersLocation = othersLocation
        self.states = []

    def __str__(self):
        self.calcualteScore()
        agentString = "---------------\n" \
                      "{}\n" \
                      "score: {}\n" \
                      "time spent (weight of edges): {}\n" \
                      "people saved: {}\n" \
                      "---------------\n".format(type(self).__name__, self.score,
                                                 self.timeSpent,
                                                 self.amountOfPeopleSaved)
        return agentString

    def calcualteScore(self):
        self.score = (self.amountOfPeopleSaved * SCORE_MULTIPLYER) - self.timeSpent

    def doNoOp(self):
        print("No-Op")

    def setOthersLocation(self, othersLocation):
        self.othersLocation = othersLocation

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

    def updateTime(self, weightOfMove):
        self.timeSpent += weightOfMove

    def act(self):
        print("------ {} ------".format(type(self).__name__))
        if not self.terminated:
            self.state.updateState()
            self.states.append(copy.deepcopy(self.state))
            if self.state.currentVertex in self.graph.broken:
                self.doNoOp()
                self.terminated = True
            else:
                self.search()
            if len(self.actionSequence) == 0:
                # self.search()
                self.terminated = len(self.actionSequence) == 0
                print("Searched, output act sequence is: " + self.strFromSequence())
            if not self.terminated and self.timeSpent + 1 < TIME_LIMIT:
                self.move()
            else:
                self.terminated = True
                print("TERMINATED\n")
        else:
            print("TERMINATED\n")

    def search(self):
        print("not yet implemented")

    def reachedGoal(self,stateOfVertexWrapper: State):
        return stateOfVertexWrapper.areAllSaved()

    def generateSequence(self, vertexWrapperCurrent: Vertex.VertexWrapper):
        if vertexWrapperCurrent.parentWraper is None:
            return []
        edge_weight = self.graph.getEdgeWeigtFromVerName(vertexWrapperCurrent.state.currentVertex.name,
                                            vertexWrapperCurrent.parentWraper.state.currentVertex.name)
        current_move = []

        current_move.append(vertexWrapperCurrent.state.currentVertex)
        current_sequence = self.generateSequence(vertexWrapperCurrent.parentWraper)
        current_sequence.extend(current_move)
        return current_sequence

    # checks if all vertexes with people are connected to the current vertex
    def impossibleToReachGoal(self, stateOfVertex):
        reachableToSave = stateOfVertex.reachableFromPosition()
        for reachable in reachableToSave.values():
            if reachable:
                return False
        return True

    def weight(self, vertexWrapper: Vertex.VertexWrapper):
        return vertexWrapper.accumelatedweight

    def saveVertexOnMove(self):
        currentVertex = self.graph.getVertexByName(self.state.currentVertex.name)
        if currentVertex is not None and currentVertex.persons > 0:
            print("Saving: " + str(self.state.currentVertex))
            self.score += self.state.currentVertex.persons
            self.amountOfPeopleSaved += currentVertex.persons
            self.state.currentVertex.persons = 0
            currentVertex.persons = 0
        self.state.saveVertex()

    def move(self):
        self.movementAmount += 1
        # print("Current sequence: " + self.translateSequenceToString(self.actionSequence))
        next_vertex = self.actionSequence[0]
        print("Current Vertex: " + str(self.state.currentVertex))
        print("Moving to: " + str(next_vertex))
        if next_vertex != self.state.currentVertex:
            self.saveVertexOnMove()
        moveCost = self.graph.getEdgeWeigtFromVerName(self.state.currentVertex.name, next_vertex.name)
        if self.state.currentVertex.isBrittle:
            self.graph.deleteVertex(self.state.currentVertex)
        self.state.currentVertex = next_vertex
        self.updateTime(moveCost)
        self.actionSequence = self.actionSequence[1:]
        if len(self.actionSequence) == 0:
            self.saveVertexOnMove()
        if self.reachedGoal(self.state) or self.impossibleToReachGoal(self.state):
            self.terminated = True

    def terminal_state(self):
        if self.state.getAllReachable() == 0:
            return True
        for state in self.states:
            if equalStates(state, self.state):
                return True








