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
    ass4.valueIteration()
    expectedValueOfPolicies = ass4.getPolicies()
    ass4.printNextPolicy()
    # print(expectedValueOfPolicies)
    print("\nSIMULATION:\n")
    edgeStatus = dict()
    for blockableEdge in graph.getAllBlockableEdges():
        userChoice = input("Do you want to block the edge connecting vertex " + blockableEdge.fromV + " and vertex " + blockableEdge.toV + "? respond with Y or N\n")
        if userChoice == 'Y':
            edgeStatus[blockableEdge] = True
        else:
            edgeStatus[blockableEdge] = False
    ass4.findGoal(edgeStatus)

    # print("End state of the graph: {}".format(Graph()))

