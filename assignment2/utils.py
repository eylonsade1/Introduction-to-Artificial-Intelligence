import copy
import sys
import os
from Graph import Graph
import networkx as nx
import matplotlib.pyplot as plt
import collections
from Vertex import Vertex
import operator
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

def getReachableToSave(vertex:Vertex):
    reachables = {}
    graph = Graph()
    toSave = graph.toSave
    vertexNumber = graph.getVertexNumber(vertex)
    dists = dijkstra(graph, vertexNumber)
    for vertexNumber in range(len(dists)):
        vertexName  = "#V{}".format(vertexNumber+1)
        vertexObject = graph.getVertexByName(vertexName)
        try:
            #this if means the vertex has peoples to save
            if not toSave[vertexObject]:
                if dists[vertexNumber] == 1e7:
                    reachables[vertexObject] = False
                else:
                    reachables[vertexObject] = True
        except: #this is because we can't know at this stage if toSave[vertexObject] is defined.
            continue
    return reachables

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

    # printSolution(graph, dist) only for debugging
    return dist

def spanning_trees(G, currentPos):
    def buidNXGraph(graph, currentPos):
        newGraph = nx.Graph()
        for vertex in graph.vertexes:
            newGraph.add_node(vertex.name, isBrittle=vertex.isBrittle, toSave=vertex.persons)
        for edge in graph.edges:
            newGraph.add_edge(edge.fromV, edge.toV, weight=1)
        # nx.draw(newGraph)
        # plt.show()
        onlyConnected = nx.node_connected_component(newGraph, currentPos)
        for vert in graph.vertexes:
            if vert.name not in onlyConnected:
                newGraph.remove_node(vert.name)
        return newGraph

    def build_tree(H, edges, currentPos):
        if nx.is_connected(H):
            yield H
        else:
            for i in range(len(edges)):
                if edges[i][0][1] not in nx.algorithms.descendants(H, edges[i][0][0]):
                    H1 = nx.Graph(H)
                    H1.add_edge(*edges[i][0], weight=int(edges[i][1]))
                    # print("*edges[i] = ", *edges[i])
                    for H2 in build_tree(H1, edges[i+1:], currentPos):
                        yield H2

    graph = buidNXGraph(G, currentPos)
    reducedGraph = reduceGraph(graph, currentPos)
    E = nx.Graph()
    E.add_nodes_from(reducedGraph)
    return build_tree(E, [(e, weight) for e, weight in nx.get_edge_attributes(reducedGraph,'weight').items()], currentPos)


def reduceGraph(G, current):
    verticesNbrittle = nx.get_node_attributes(G, 'isBrittle')
    verticesNpeople = nx.get_node_attributes(G, 'toSave')
    for vertex in verticesNbrittle:
        if not bool(verticesNbrittle[vertex]) and int(verticesNpeople[vertex]) < 1 and not str(vertex) == current:
            neighbors = nx.all_neighbors(G, vertex)
            for neighbor1 in neighbors:
                # todo verify issue here
                for neighbor2 in neighbors:
                    # if neighbor1 not in G[neighbor2].keys():
                    # weight1 = Graph().getEdgeWeigtFromVerName(neighbor1)
                    newWeight = int(G.edges[vertex, neighbor1]['weight']) + int(G.edges[vertex, neighbor2]['weight'])
                    G.add_edge(neighbor1, neighbor2, weight=newWeight)
                    # else:
                    #     newWeight = neighbors[neighbor1] + neighbors[neighbor2]
                    #     G.add_edge(neighbor1, neighbor2, weight=newWeight)

            G.remove_node(vertex)
   # printGraph(newGraph)
    return G


def printGraph(graph):
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos, with_labels=True, font_weight='bold')
    weightLabels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=weightLabels)
    plt.show()


# get the minimum weight of a path in tree that saves all people
def minTree(graphs, currentPos, currentState):
    realGraph = Graph()
    bestWeight = None
    bestWeightNotValid = None
    # toTravel = all nodes with people to save
    allToSave = currentState.getAllToSaveByName()
    toTravel = copy.copy(allToSave)
    # add the current position to the vertexes that need to be in path
    if currentPos not in toTravel:
        toTravel.append(currentPos)
    toTravel.append("#VV")
    # go over all generated tree graphs (from spanning_trees)
    for graph in graphs:
        # weight for the edge connecting the fake node to start position - vertex '#VV'
        graphWeightExtra = graph.size(weight="weight")
        # connect non-existing node to current position - control starting position of path
        graph.add_node("#VV")
        graph.add_edge("#VV", currentPos, weight=graphWeightExtra)
        # make a list with vertexes with people to save & that are reachable from current position
        toTravelReal = copy.copy(toTravel)
        reachableOrNot = dict()
        for vertex in toTravel:
            if not vertex == "#VV":
                vertexObj = realGraph.getVertexByName(vertex)
                if vertex in allToSave:
                    if not graph.has_node(vertex):
                        toTravelReal.remove(vertex)
                        reachableOrNot[vertexObj] = False
                    else:
                         reachableOrNot[vertexObj] = True
        # update in state for current vertex: {vertexToSave1: bool (indicates if reachable or not), ...}
        currentState.setReachableFromVertex(reachableOrNot)
        # approximate path & get the path's weight
        path = nx.approximation.traveling_salesman_problem(graph, nodes=toTravelReal, cycle=False)
        graphWeight = nx.path_weight(graph, path, weight="weight")
        # check if a brittle node is passed twice in the path
        doubles = [item for item, count in collections.Counter(path).items() if count > 1]
        valid = True
        for vertex in doubles:
            if realGraph.checkIfBrittle(vertex):
                valid = False
        # reduce the extra weight from the non-existing vertex (added before)
        graphWeight -= graphWeightExtra
        # save minimum value of a valid path
        if (bestWeight is None or bestWeight > graphWeight) and valid:
            # bestTree = graph
            bestWeight = graphWeight
        # save minimum value of a non-valid path (in case there isn't a valid one)
        elif (bestWeightNotValid is None or bestWeightNotValid > graphWeight) and not valid:
            bestWeightNotValid = graphWeight
    # return the minimum valid path weight if exists, else return the minimum non-valid path
    if bestWeight is not None:
        return bestWeight
    else:
        return bestWeightNotValid

def vector_add(a, b):
    """Component-wise addition of two vectors."""
    return tuple(map(operator.add, a, b))

if __name__ == '__main__':
    createGraph(os.path.join(os.getcwd(), 'graph.csv'))
    print(Graph().adjMatrix)
    getReachableToSave(Graph().getVertexByName("#V1"))
    # s = spanning_trees(Graph(), "#V1")
    # minWeight = minTree(s, "#V1")


