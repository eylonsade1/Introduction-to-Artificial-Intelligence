import os
from Assignment import Assignmen2
import OutputStrings as out
from Graph import Graph
def createGraph(pathToGraph):
    if os.path.isfile(pathToGraph):
        graph = Graph()
        graph.readCsvFillInfo(pathToGraph)
        graph.buildMatrix()
    else:
        print(out.FILE_DOESNT_EXIST)
    print(out.GRAPH_FINISHED)

if __name__ == '__main__':
    createGraph(os.path.join(os.getcwd(), 'graph.csv'))
    ass2 = Assignment1()
    ass2.userInit()
    ass2.runAgents()
    ass2.printAgentsState()
    print("End state of the graph: {}".format(Graph()))

