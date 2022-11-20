import os

class assignment1(object):
    def __init__:
        self.graph = None
    def readGraph(self, pathToGraph):
        if os.path.isfile(pathToGraph):
            with open ('a', pathToGraph) as graophFile:


if __name__ == 'main':
    ass1 = assignment1()
    ass1.readGraph(os.path.join(os.getcwd(), 'graph.csv'))
    