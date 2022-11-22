import os
from Assignment import Assignment1
import OutputStrings as out
from Graph import Graph
def createGraph(pathToGraph):
    if os.path.isfile(pathToGraph):
        graph = Graph()
        graph.readCsvFillInfo(pathToGraph)
    else:
        print(out.FILE_DOESNT_EXIST)
    print(out.GRAPH_FINISHED)

if __name__ == '__main__':
    createGraph(os.path.join(os.getcwd(), 'graph.csv'))
    ass1 = Assignment1()
    ass1.userInit()
    # program

