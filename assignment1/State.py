from Graph import Graph

class State(object):
    def __init__(self, currentVertex, brokenVertexes, vertexWithPeopleToSave):
        self.currentVertex = currentVertex

        #############################################
        # SingleImplementation - to consider change #
        #############################################
        self.broken = brokenVertexes
        self.toSave = vertexWithPeopleToSave
        self.graph = Graph()

        #################################
        # None singleton implemantation #
        #################################
        # self.graph = graph

    def __str__(self):
        return "Current position: {} in the environment: \n{}\n".format(self.currentVertexstr, (self.graph))
