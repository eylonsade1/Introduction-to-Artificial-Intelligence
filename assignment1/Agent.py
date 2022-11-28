from collections import defaultdict
import Vertex
from Graph import Graph
from State import State
from PriorityQueue import PriorityQueue
import copy

SCORE_MULTIPLYER = 1000
GREEDY_LIMIT = 1
A_STAR_LIMIT = 10000
A_START_DEPTH_LIMIT = 10
TIME_LIMIT = 400

class Agent(object):
    def __init__(self, startingPosition):
        self.score = 0
        self.amountOfPeopleSaved = 0
        self.timeSpent = 0
        self.terminated = False
        self.graph = Graph()
        self.state = State(self.graph.vertexes[startingPosition], self.graph.getAllToSave())
        # new - to test
        self.expansionsAmount = 0
        self.movementAmount = 0

    def calcualteScore(self):
        self.score = (self.amountOfPeopleSaved * SCORE_MULTIPLYER) - self.timeSpent

    def move(self):
        print("not yet implemented for this agent")

    #todo connect update time instead of 1 update each move
    def updateTime(self, weightOfMove):
        self.timeSpent += weightOfMove

    def BFSShortestPath(self, adjMet, start, goal):
        explored = []

        # Queue for traversing the graph in the BFS
        queue = [[start]]

        # If the desired node is reached
        if start == goal:
            return start, 0

        # Loop to traverse the graph with the help of the queue
        while queue:
            path = queue.pop(0)
            node = path[-1]

            # Condition to check if the current node is not visited
            if node not in explored:
                neighbours = adjMet[node]

                # Loop to iterate over the neighbours of the node
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

                    # Condition to check if the neighbour node is the goal
                    if neighbour == goal:
                        return new_path, len(new_path)
                explored.append(node)

        # nodes aren't connected
        return None, None


    def __str__(self):
        self.calcualteScore()
        agentString = "---------------\n" \
                      "{}\n" \
                      "score: {}\n" \
                      "time spent (weight of edges): {}\n" \
                      "expansions performed: {}\n" \
                      "people saved: {}\n" \
                      "---------------\n".format(type(self).__name__, self.score,
                                                 self.timeSpent, self.expansionsAmount,
                                                 self.amountOfPeopleSaved)
        return agentString


class StupidGreedy(Agent):
    def __init__(self, startingPosition):
        super(StupidGreedy, self).__init__(startingPosition)
        print("stupid greedy constructor called")

    def move(self):
        if not self.terminated:
            if not self.computerShortestPath():
                self.terminated = True
        else:
            print("Stupid greedy agent cannot move - terminated")

    def computerShortestPath(self):
        return


class Saboteur(Agent):
    def __init__(self, startPosition: Vertex.Vertex):
        super(Saboteur, self).__init__(startPosition)

    def breakV(self, vertexName):
        vertex = self.graph.getVertexByName(vertexName)
        if None:
            print("Error!! This shouldn't happen")
        vertex.isBlocked = True
        self.graph.deleteVertex(vertex)

    def move(self):
        path, dist = self.search(self.state.currentVertex)
        if path is None:
            self.terminated = True
            # todo: Do no-op + print
        elif dist == 2:  # path of length 1 - move one vertex then break it
            self.state.currentVertex = path[1]
            self.breakV(path[1])
            # todo: print
        else:  # move to next vertex, don't break it
            self.state.currentVertex = path[1]
            # todo: print

    def search(self):
        startPosition = self.state.currentVertex
        brittles = self.graph.getAllBrittle()
        if len(brittles) == 0:
            return None
        minDist = None
        path = None
        adjMet = self.buildAdjMatrix(self.graph)
        startPos = startPosition.name
        for vertex in brittles:
            newPath, dist = self.BFSShortestPath(adjMet, startPos, vertex.name)
            if newPath is None:
                continue
            elif path is None or minDist > dist or (minDist == dist and newPath[1][2] < path[1][2]):
                minDist = dist
                path = newPath
        return path, minDist

    def buildAdjMatrix(self, graph):
        adjMet = defaultdict(list)
        for edge in graph.edges:
            a = edge.toV
            b = edge.fromV
            adjMet[a].append(b)
            adjMet[b].append(a)
        return adjMet


class HumanAgent(Agent):
    def __init__(self, startingPosition):
        super(HumanAgent, self).__init__(startingPosition)
        print("Human constructor called")

    def move(self):
        print("Current agent state : {}".format(self.state))


class AIAgent(Agent):
    def __init__(self, h, startingPosition, movesLimit):
        self.actionSequence = []
        self.heauristic = h
        self.movesLimit = movesLimit
        super(AIAgent, self).__init__(startingPosition)


    def strFromSequence(self):
        sequenceString = "["
        for vertex in self.actionSequence:
            sequenceString += str(vertex)
        sequenceString += "]"
        return sequenceString

    def act(self):
        print("------ {} ------".format(type(self).__name__))
        if not self.terminated:
            self.state.updateState()
            if len(self.actionSequence) == 0:
                self.search()
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
        for i in range(edge_weight):
            current_move.append(vertexWrapperCurrent.state.currentVertex)
        current_sequence = self.generateSequence(vertexWrapperCurrent.parentWraper)
        current_sequence.extend(current_move)
        return current_sequence


    # def impossibleToReachGoal(self, stateOfVertex):


    def limitedSearch(self, fringe):
        counter = 0
        vertexWrapperSelf = Vertex.VertexWrapper(copy.copy(self.state), None, 0)
        fringe.insert(vertexWrapperSelf)
        while not fringe.is_empty():
            vertexWrapperCurrent = fringe.pop()
            current_vertex = vertexWrapperCurrent.state.currentVertex
            acc_weight = vertexWrapperCurrent.accumelatedweight
            vertexWrapperCurrent.state.saveVertex()
            if counter == self.movesLimit or self.reachedGoal(vertexWrapperCurrent.state): #or self.impossibleToReachGoal(vertexWrapperCurrent.state):
                self.actionSequence = self.generateSequence(vertexWrapperCurrent)
                break
            counter += 1
            for neighbor_tup in self.graph.getNeighborsList(current_vertex):
                neighbor_state = State(neighbor_tup[0], copy.copy(vertexWrapperCurrent.state.toSave))
                neighbor_vertex_wrapper = Vertex.VertexWrapper(neighbor_state, vertexWrapperCurrent,
                                                          acc_weight + neighbor_tup[1])
                fringe.insert(neighbor_vertex_wrapper)
        self.expansionsAmount += counter
        return counter

    def weight(self, vertexWrapper: Vertex.VertexWrapper):
        return vertexWrapper.accumelatedweight

    #todo : casuses crash because moving from same vertex to same vertex - tofix heaurstic to avoid issue here
    def saveVertexOnMove(self):
        currentVertex = self.graph.getVertexByName(self.state.currentVertex.name)
        if currentVertex.persons > 0:
            print("Saving: " + str(self.state.currentVertex))
            self.score += self.state.currentVertex.persons
            self.amountOfPeopleSaved += currentVertex.persons
            self.state.currentVertex.persons = 0
            currentVertex.persons = 0

    def translateSequenceToString(self, actionSequence):
        s = "[ "
        for vertex in actionSequence:
            s += str(vertex) + ", "
        last_index_of_comma = s.rfind(",")
        if last_index_of_comma != -1:
            s = s[:last_index_of_comma] + s[last_index_of_comma + 1:]
        return s + "]"

    def move(self):
        self.movementAmount += 1
        print("Current sequence: " + self.translateSequenceToString(self.actionSequence))
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


class greedyAgent(AIAgent):
    def __init__(self, h, startingPosition):
        super(greedyAgent, self).__init__(h, startingPosition, GREEDY_LIMIT)

    def search(self):
        fringe = PriorityQueue(self.heauristic)
        return self.limitedSearch(fringe)


class AStarAgent(AIAgent):
    def __init__(self,h ,startingPosition):
        super(AStarAgent, self).__init__(h, startingPosition, A_STAR_LIMIT)

    def search(self):
        fringe = PriorityQueue(lambda x: self.heauristic(x) + self.weight(x))
        return self.limitedSearch(fringe)


class AStarAgentDepth(AIAgent):
    def __init__(self, h, startingPosition):
        super(AStarAgentDepth, self).__init__(h, startingPosition, A_START_DEPTH_LIMIT)

    def search(self):
        fringe = PriorityQueue(lambda x: self.heauristic(x) + self.weight(x))
        return self.limitedSearch(fringe)



