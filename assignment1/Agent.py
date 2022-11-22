import sys
from collections import defaultdict
import Vertex
import Graph
from State import State
import os
import utils

SCORE_MULTIPLYER = 1000


class Agent(object):
    def __init__(self, startingPosition):
        self.score = 0
        self.amountOfPeopleSaved = 0
        self.timeSpent = 0
        self.terminated = False
        self.state = State(startingPosition)
        self.graph = Graph()

    def calcualteScore(self):
        self.score = (self.amountOfPeopleSaved * SCORE_MULTIPLYER) - self.timeSpent

    def move(self, observations):
        print("not yet implemented for this agent")


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


class StupidGreedy(Agent):
    def __init__(self):
        super(StupidGreedy, self).__init__()
        print("stupid greedy constructor called")

    def move(self, observations):
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


class AIAgent(Agent):
    def __init__(self, h):
        self.heauristic = h



