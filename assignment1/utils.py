import sys
import os
from Graph import Graph

def createGraph(pathToGraph):
    if os.path.isfile(pathToGraph):
        graph = Graph()
        graph.readCsvFillInfo(pathToGraph)
        graph.buildMatrix()

def printSolution(graph, dist):
    print("Vertex \t Distance from Source")
    for node in range(len(graph.vertexes)):
        print(node, "\t\t", dist[node])


def minDistance(graph, dist, sptSet):
    min = sys.maxsize
    for vertex in range(len(graph.vertexes)):
        if dist[vertex] < min and sptSet[vertex] == False:
            min = dist[vertex]
            min_index = vertex

    return min_index


def dijkstra(graph, src):
    dist = [1e7] * len(graph.vertexes)
    dist[src] = 0
    sptSet = [False] * len(graph.vertexes)

    for cout in range(len(graph.vertexes)):
        u = minDistance(graph, dist, sptSet)
        sptSet[u] = True
        for v in range(len(graph.vertexes)):
            if (graph.adjMatrix[u][v] > 0 and
                    sptSet[v] == False and
                    dist[v] > dist[u] + graph.adjMatrix[u][v]):
                dist[v] = dist[u] + graph.adjMatrix[u][v]

    printSolution(graph, dist)

if __name__ == '__main__':
   createGraph(os.path.join(os.getcwd(), 'graph.csv'))
   print(Graph().adjMatrix)
   dijkstra(Graph(),0)