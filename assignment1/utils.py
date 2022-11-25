import sys
import os
from Graph import Graph
import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy

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


def spanning_trees(G):
    def buidNXGraph(graph):
        newGraph = nx.Graph()
        for vertex in graph.vertexes:
            newGraph.add_node(vertex.name)
        for edge in graph.edges:
            newGraph.add_edge(edge.fromV, edge.toV, weight=edge.weight)
        # nx.draw(newGraph)
        # plt.show()
        return newGraph

    def build_tree(H, edges):
        if nx.is_connected(H):
            yield H
        else:
            for i in range(len(edges)):
                if edges[i][1] not in nx.algorithms.descendants(H, edges[i][0]):
                    H1 = nx.Graph(H)
                    H1.add_edge(*edges[i])
                    for H2 in build_tree(H1, edges[i+1:]):
                        yield H2

    graph = buidNXGraph(G)
    reducedGraph = reduceGraph(graph)
    E = nx.Graph()
    E.add_nodes_from(reducedGraph)
    return build_tree(E, [e for e in reducedGraph.edges])


def reduceGraph(G):
    newGraph = deepcopy(G)
    # weights = nx.get_edge_attributes(G, 'weight')
    for vertex in nx.nodes(G):
        if vertex not in Graph().getAllBrittleNames() and vertex not in Graph().getAllToSaveNames():
            neighbors = nx.all_neighbors(newGraph, vertex)
            print("neighbors",vertex, *neighbors)
            for neighbor1 in neighbors:
                for neighbor2 in neighbors:
                    if neighbor1 not in G[neighbor2].keys():
                        newWeight = neighbors[neighbor1] + neighbors[neighbor2]
                        newGraph.add_edge(neighbor1, neighbor2, weight=newWeight)
            newGraph.remove_node(vertex)
    return newGraph
                # neighbor2 = G[neighbor1].keys()
                #
                # weights = nx.get_edge_attributes(G, 'weight')
                # print("weight", weight1)
                # print("neighbor1", neighbor1, G[neighbor1])
                # for neighbor2 in reversed(neighbors):
                #     if neighbor1 is neighbor2:
                #         stop = True
                #     else:
                #         G.add_edge(neighbor1, neighbor2)






if __name__ == '__main__':
    createGraph(os.path.join(os.getcwd(), 'graph.csv'))
    print(Graph().adjMatrix)
    dijkstra(Graph(),0)
    s = spanning_trees(Graph())
    for tree in s:
        nx.draw(next(s))
        plt.show()


