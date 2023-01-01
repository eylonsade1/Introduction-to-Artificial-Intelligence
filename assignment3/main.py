import os
from Assignment import Assignment3
from Graph import Graph
import OutputStrings as out

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
    ass3 = Assignment3()
    print("End state of the graph: {}".format(Graph()))

