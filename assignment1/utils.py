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


def spanning_trees(G, currentPos):
    def buidNXGraph(graph):
        newGraph = nx.Graph()
        for vertex in graph.vertexes:
            newGraph.add_node(vertex.name, isBrittle=vertex.isBrittle, toSave=vertex.persons)
        for edge in graph.edges:
            newGraph.add_edge(edge.fromV, edge.toV, weight=edge.weight)
        # nx.draw(newGraph)
        plt.show()
        return newGraph

    def build_tree(H, edges, currentPos):
        if nx.is_connected(H):
            yield H
        else:
            for i in range(len(edges)):
                if edges[i][0][1] not in nx.algorithms.descendants(H, edges[i][0][0]):
                    H1 = nx.Graph(H)
                    H1.add_edge(*edges[i][0], weight=edges[i][1])
                    # print("*edges[i] = ", *edges[i])
                    for H2 in build_tree(H1, edges[i+1:], currentPos):
                        yield H2

    graph = buidNXGraph(G)
    reducedGraph = reduceGraph(graph, "#V1")
    E = nx.Graph()
    E.add_nodes_from(reducedGraph)
    return build_tree(E, [(e, weight) for e, weight in nx.get_edge_attributes(reducedGraph,'weight').items()], currentPos)


def reduceGraph(G, current):
    # newGraph = deepcopy(G)
    verticesNweight = nx.get_node_attributes(G, 'isBrittle')
    verticesNpeople = nx.get_node_attributes(G, 'toSave')
    print("verticesNweight", verticesNweight)
    print("verticesNpeople", verticesNpeople)
    for vertex in verticesNweight:
        print("vertex", vertex)
        if not bool(verticesNweight[vertex]) and int(verticesNpeople[vertex]) < 1 and not str(vertex) == current:
            neighbors = nx.all_neighbors(G, vertex)
            print("neighbors",vertex, *neighbors)
            for neighbor1 in neighbors:
                for neighbor2 in neighbors:
                    if neighbor1 not in G[neighbor2].keys():
                        newWeight = neighbors[neighbor1] + neighbors[neighbor2]
                        G.add_edge(neighbor1, neighbor2, weight=newWeight)
            G.remove_node(vertex)
   # printGraph(newGraph)
    return G


def printGraph(graph):
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos, with_labels=True, font_weight='bold')
    weightLabels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=weightLabels)
    plt.show()


def minTree(graphs):
    bestTree = None
    bestWeight = None
    for graph in graphs:
        graphWeight = graph.size(weight="weight")
        if bestTree is None or bestWeight > graphWeight: # todo: check if brittle node is visited twice
            bestTree = graph
            bestWeight = graphWeight
    return bestTree


if __name__ == '__main__':
    createGraph(os.path.join(os.getcwd(), 'graph.csv'))
    print(Graph().adjMatrix)
    dijkstra(Graph(),0)
    s = spanning_trees(Graph(), "#V1")
    # print("next(s) = ", next(s))
    while s:
        g = next(s)
        print(g)
        printGraph(g)


