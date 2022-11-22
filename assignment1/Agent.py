from collections import defaultdict
import Vertex
import Graph

SCORE_MULTIPLYER = 1000


class Agent(object):
    def __init__(self, startingPosition):
        self.score = 0
        self.amountOfPeopleSaved = 0
        self.timeSpent = 0
        self.terminated = False
        self.state = None
        self.graph = Graph()

    def calcualteScore(self):
        self.score = (self.amountOfPeopleSaved * SCORE_MULTIPLYER) - self.timeSpent

    def move(self, observations):
        print ("not yet implemented for this agent")

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
    def __init__(self, startPosition: Vertex.Vertex, graph: Graph.Graph):
        super(Saboteur, self).__init__(startPosition, graph)

    def move(self):
        path, dist = self.search(self.startPosition)
        if path is None:
            return
        elif dist == 1:  # break current node - Block
            5
        else:  # move to next vertex
            self.startPosition = path

    def search(self, startPosition: Vertex.Vertex):
        brittles = self.graph.getAllBrittle()
        if len(brittles) == 0:
            return None
        minDist = None
        path = None
        adjMet = self.buildAdjMet(self.graph)
        startPos = startPosition.name
        for vertex in brittles:
            newPath, dist = self.BFS_SP(adjMet, startPos, vertex.name)
            if newPath is None:
                continue
            elif path is None or minDist > dist or (minDist == dist and newPath[1][2] < path[1][2]):
                minDist = dist
                path = newPath
        return path, minDist

    def buildAdjMatrix(self, graph):
        adjMet = defaultdict(list)
        for edge in graph.edges:
            a = "#V" + edge.toV
            b = "#V" + edge.fromV
            adjMet[a].append(b)
            adjMet[b].append(a)
        return adjMet


class AIAgent(Agent):
    def __init__(self, h):
        self.heauristic = h
