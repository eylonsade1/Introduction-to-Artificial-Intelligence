import os
from Assignment import Assignment3
from Graph import Graph
import OutputStrings as out
from BayesNetwork import BayesNetwork

def createGraph(pathToGraph):
    if os.path.isfile(pathToGraph):
        graph = Graph()
        graph.readCsvFillInfo(pathToGraph)
        graph.buildMatrix()
    else:
        print(out.FILE_DOESNT_EXIST)
    print(out.GRAPH_FINISHED)

def createBayesNetwork():
    bayersNetwork = BayesNetwork()
    bayersNetwork.createWeatherNodes()
    bayersNetwork.createBlockedNodes()
    bayersNetwork.createEvacueeNodes()


if __name__ == '__main__':
    createGraph(os.path.join(os.getcwd(), 'graph.csv'))
    createBayesNetwork()
    ass3 = Assignment3()
    print("End state of the graph: {}".format(Graph()))

