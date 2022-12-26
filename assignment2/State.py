import copy

from Graph import Graph
import utils


class State(object):
    def __init__(self, currentVertex, vertexWithPeopleToSave, brokenVertexes, othersLocation):
        self.currentVertex = currentVertex
        self.toSave = vertexWithPeopleToSave
        self.graph = Graph()
        self.reachable = utils.getReachableToSave(currentVertex)
        self.brokenVertexes = brokenVertexes
        self.othersLocation = othersLocation
        self.minScore = 0
        self.maxScore = 0

    def __str__(self):
        return "Current position: {} in the environment: \n{}\n".format(self.currentVertexstr, (self.graph))

    def updateState(self):
        graphState = self.graph.getAllToSave()
        self.brokenVertexes = self.graph.getAllBroken()
        for vertex in graphState:
            if graphState[vertex]:
                self.toSave[vertex] = True
            else:
                self.toSave[vertex] = False

    def saveVertex(self):
        self.toSave[self.currentVertex] = True

    def areAllSaved(self):
        for vertex in self.toSave:
            if not self.toSave[vertex]:
                return False
        return True

    def reachableFromPosition(self):
        return self.reachable

    def setReachableFromVertex(self, reachableList):
        self.reachable = reachableList

    def getAllToSaveByName(self):
        needSave = []
        for key, value in self.toSave.items():
            if not value:
                needSave.append(key.name)
        return needSave

    def getCurrentLocation(self):
        return self.currentVertex

    def getAllReachable(self):
        return self.reachable

    def getAllBrokenVertexes(self):
        return self.brokenVertexes

    def getOthersLocation(self):
        return self.othersLocation

    def successor(self, type_of_agent: str, graph: Graph):
        if type_of_agent == 1: # Max
            return self.maxSuccessor(graph)
        else: # Min
            return self.min_successor(graph)
        
    def maxSuccessor(self, graph):
        newStates = []
        # if self.max_agent_current_location.edge_progress > 0:
        #     new_state = self.get_new_state()
        #     new_state.max_agent_current_location = new_state.max_agent_current_location.get_new_closer_location()
        #     new_state.simulated_movements += 1
        #     new_states.append(new_state)
        #     if new_state.max_agent_current_location.edge_progress == 0:
        #         if not new_state.vertices_status[new_state.max_agent_current_location.successor]:
        #             max_new_score = new_state.max_agent_score + new_state.max_agent_current_location.successor.num_of_people
        #             new_state.mark_save_vertex(new_state.max_agent_current_location.successor)
        #             new_state.max_agent_score = max_new_score
        # else:
        # arrived_to_vertex = self.max_agent_current_location.successor
        for neighbour in graph.expand(self.currentVertex):
            max_new_score = self.max_agent_score
            # progress = neighbour[1] - 1 this is for edgfe weight > 1
            # max_new_location = Location(arrived_to_vertex, progress, neighbour[0])
            new_state = copy.deepcopy(self)
            new_state.simulated_movements += 1
            # if progress == 0: this is for edgfe weight > 1
            if not new_state.vertices_status[neighbour[0]]:
                max_new_score = self.max_agent_score + neighbour[0].num_of_people
                new_state.mark_save_vertex(neighbour[0])
            # new_state.max_agent_current_location = max_new_location
            new_state.max_agent_score = max_new_score
            newStates.append(new_state)
        return newStates
