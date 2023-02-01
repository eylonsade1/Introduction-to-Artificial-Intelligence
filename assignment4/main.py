import os
from Assignment import Assignment
import OutputStrings as out
from Graph import Graph
import State
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
    graph = Graph()
    states = State.generateAllStates()
    ass4 = Assignment(states)
    expectedValueOfPolicies = ass4.valueIteration()
    expectedValueOfPolicies = ass4.getPolicies()
    # ass1.runAgents()
    # ass1.printAgentsState()
    print("End state of the graph: {}".format(Graph()))

