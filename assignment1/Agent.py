from collections import defaultdict
import Vertex
import Graph
from State import State

SCORE_MULTIPLYER = 1000


class Agent(object):
    def __init__(self, startingPosition, graph):
        self.score = 0
        self.amountOfPeopleSaved = 0
        self.timeSpent = 0
        self.terminated = False
        self.state = State(startingPosition)
        self.graph = graph

    def calcualteScore(self):
        self.score = (self.amountOfPeopleSaved * SCORE_MULTIPLYER) - self.timeSpent

    def moveToPerform(self, observations):
        print ("not yet implemented for this agent")


class StupidGreedy(Agent):
    def __init__(self):
        super(StupidGreedy, self).__init__()
        print("stupid greedy constructor called")

    def moveToPerform(self, observations):
        return


class Saboteur(Agent):
    def __init__(self, startPosition: Vertex.Vertex, graph: Graph.Graph):
        super(Saboteur, self).__init__(startPosition, graph)

    def move(self):
        path, dist = self.search(self.state.currentVertex)
        if path is None:
            self.terminated = True
            # todo: Do no-op
        elif dist == 1:  # break current node - Block
            5
        else:  # move to next vertex
            self.startPosition = path

    def buildAdjMatrix(self, graph):
        adjMet = defaultdict(list)
        for edge in graph.edges:
            a = "#V" + edge.toV
            b = "#V" + edge.fromV
            adjMet[a].append(b)
            adjMet[b].append(a)
        return adjMet

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
                        print(*new_path)
                        return new_path, len(new_path)
                explored.append(node)

        # nodes aren't connected
        return None, None

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

class AIAgent(Agent):
    def __init__(self, h):
        self.heauristic = h
