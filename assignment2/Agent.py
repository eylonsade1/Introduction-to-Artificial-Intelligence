import Vertex
from Graph import Graph
from State import State
import games
import copy

TIME_LIMIT = 400

class Agent(object):
    def __init__(self, startingPositionMax, startingPositionMin, utilityFunction=None, doPrune=False):
        self.graph = Graph()
        #todo - add handling of new state structure
        self.state = None #State(self.graph.vertexes[startingPosition], self.graph.getAllToSave())
        self.actionSequence = [startingPositionMax, 0, startingPositionMax]
        self.utilityFunction = utilityFunction
        self.prune = doPrune
        self.movementAmount = 0
        self.timeSpent = 0
        self.individualScore = 0
        self.totalScore = 0
        self.otherAgent = None
        self.terminated = False

    def __str__(self):
        agentString = "---------------\n" \
                      "{}\n" \
                      "people saved: {}\n" \
                      "time spent (weight of edges): {}\n" \
                      "score(total) {}\n" \
                      "---------------\n".format(type(self).__name__, self.individualScore,
                                                 self.timeSpent, self.totalScore)
        return agentString

    def doNoOp(self):
        print("No-Op")

    def strFromSequence(self):
        sequenceString = "["
        for vertex in self.actionSequence:
            sequenceString += str(vertex)
        sequenceString += "]"
        return sequenceString

    def translateSequenceToString(self, actionSequence):
        s = "[ "
        for vertex in actionSequence:
            s += str(vertex) + ", "
        last_index_of_comma = s.rfind(",")
        if last_index_of_comma != -1:
            s = s[:last_index_of_comma] + s[last_index_of_comma + 1:]
        return s + "]"

    def set_new_location(self, location_params):
        pass

    def miniMax(self, state: State):
        return []

    def minimax_alpha_beta(self, state: State):
        return []

    def update_state(self):
        pass

    #@todo add understading if a state has already happend or if all people are saved
    def shouldTerminateGame(self):
        return self.graph.areAllSaved()

    def act(self):
        print("------ {} ------".format(type(self).__name__))
        self.terminated = self.shouldTerminateGame()
        if not self.terminated:
            if self.actionSequence[1] > 0 and self.movementAmount < TIME_LIMIT:
                self.move()
            elif self.movementAmount >= TIME_LIMIT:
                self.terminated = True
                print("TERMINATED\n")
            elif self.actionSequence[1] == 0:
                self.updateState()
                print("MINIMAXING")
                #todo implement minimax alfaBeta and pruning on games.py
                self.act_sequence = self.miniMax(self.state, self.prune)
                # self.act_sequence = games.minimax_alpha_beta(self.state)
                self.actionSequence.append(self.act_sequence[2])
                # self.set_new_location(self.act_sequence)
                self.move()
        else:
            print("TERMINATED\n")


    def impossibleToReachGoal(self, stateOfVertex):
        reachableToSave = stateOfVertex.reachableFromPosition()
        for reachable in reachableToSave.values():
            if reachable:
                return False
        return True

    def weight(self, vertexWrapper: Vertex.VertexWrapper):
        return vertexWrapper.accumelatedweight

    def saveVertexOnMove(self):
        currentVertex = self.graph.getVertexByName(self.state.currentVertex.name)
        if currentVertex is not None and currentVertex.persons > 0:
            print("Saving: " + str(self.state.currentVertex))
            self.individualScore += currentVertex.persons
            self.state.currentVertex.persons = 0
            currentVertex.persons = 0
        self.state.saveVertex()

    def move(self):
        self.movementAmount += 1
        next_vertex = self.actionSequence[0]
        print("Current Vertex: " + str(self.state.currentVertex))
        print("Moving to: " + str(next_vertex))
        if next_vertex != self.state.currentVertex:
            self.saveVertexOnMove()
        #todo - always 1
        moveCost = self.graph.getEdgeWeigtFromVerName(self.state.currentVertex.name, next_vertex.name)
        if self.state.currentVertex.isBrittle:
            self.graph.deleteVertex(self.state.currentVertex)
        self.state.currentVertex = next_vertex
        self.timeSpent += 1
        self.actionSequence = self.actionSequence[1:]
        if len(self.actionSequence) == 0:
            self.saveVertexOnMove()
        #todo add termination based on the state
        # if self.reachedGoal(self.state) or self.impossibleToReachGoal(self.state):
        #     self.terminated = True

    #@todo add state update method - based on relevant state behavior - state recieves
    def updateState(self):
        print ("Not yet implemented")

    def max_value_alpha_beta(self, state, num_of_plys, alpha, beta):
        if state.terminal_state(num_of_plys):
            return state.evaluate_alpha_beta()
        v = float('-inf')
        for next_state in state.successor("MAX"):
            v = max(v, self.min_value_alpha_beta(next_state, num_of_plys + 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value_alpha_beta(self, state: State, num_of_plys, alpha, beta):
        if state.terminal_state(num_of_plys):
            return state.evaluate_alpha_beta()
        v = float('inf')
        for next_state in state.successor("MIN"):
            v = min(v, self.max_value_alpha_beta(next_state, num_of_plys + 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

class maxAgent(Agent):
    def __init__(self, startingPosition, agentType, utilityFunction=None, doPrune=False):
        super(maxAgent, self).__init__(startingPosition, agentType, utilityFunction, doPrune)

    def set_new_location(self, location_params):
        self.state.max_agent_current_location.set_location_parameters(location_params[0], location_params[1],
                                                                      location_params[2])

    def updateState(self):
        return
        # self.state.min_agent_current_location = self.other_agent.state.min_agent_current_location
        # self.state.update_vertices_status()
        # self.state.max_agent_score = self.totalScore
        # self.state.min_agent_score = self.otherAgent.totalScore
        # self.state.simulated_movements = Agent.num_of_real_movements


    def max_value(self, state, num_of_plys, WORLD: Graph):
        if state.terminal_state(num_of_plys):
            return state.evaluate()
        best_value = None
        for next_state in state.successor("MAX", WORLD):
            next_state_min_value = self.min_value(next_state, num_of_plys + 1, WORLD)
            if best_value is None:
                best_value = next_state_min_value
            best_value = self.utilityFunction(best_value, next_state_min_value)
        return best_value


    def min_value(self, state: State, num_of_plys, WORLD: Graph):
        if state.terminal_state(num_of_plys):
            return state.evaluate()
        best_value = None
        for next_state in state.successor("MIN", WORLD):
            next_state_max_value = self.max_value(next_state, num_of_plys + 1, WORLD)
            if best_value is None:
                best_value = next_state_max_value
            best_value = self.otherAgent.utilityFunction(best_value, next_state_max_value)
        return best_value


    def miniMax(self, state: State, WORLD: Graph):
        best_value = None
        best_edge = None
        num_of_plys = 0
        for next_state in state.successor("MAX", WORLD):
            value_of_new_state = self.min_value(next_state, num_of_plys + 1, WORLD)
            current_edge = self.graph.get_edge(next_state.max_agent_current_location.prev,
                                          next_state.max_agent_current_location.successor)
            if best_value is None:
                best_value = value_of_new_state
                best_edge = current_edge
            elif not (best_value == self.comparator(best_value, value_of_new_state)):
                best_value = value_of_new_state
                best_edge = current_edge
        return [best_edge[0], best_edge[1], best_edge[2]]


    def minimax_alpha_beta(self, state: s.State, WORLD: Graph):
        best_edge = None
        num_of_plys = 0
        v = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for next_state in state.successor("MAX", WORLD):
            value_of_new_state = self.min_value_alpha_beta(next_state, num_of_plys + 1, WORLD, alpha, beta)
            current_edge = WORLD.get_edge(next_state.max_agent_current_location.prev,
                                          next_state.max_agent_current_location.successor)
            if v < value_of_new_state:
                v = value_of_new_state
                best_edge = current_edge
            alpha = max(v, alpha)
        return [best_edge[0], best_edge[1], best_edge[2]]

class MinAgent(Agent):
    def __init__(self, startingPosition, utilityFunction=None, doPrune=False):
        super(MinAgent, self).__init__(startingPosition, utilityFunction, doPrune)

    def set_new_location(self, location_params):
        self.state.min_agent_current_location.set_location_parameters(location_params[0], location_params[1], location_params[2])

    def updateState(self):
        # self.state.max_agent_current_location = self.otherAgent.state.max_agent_current_location
        # self.state.update_vertices_status()
        # self.state.simulated_movements = self.movementAmount
        # self.state.max_agent_score = self.otherAgent.real_score
        # self.state.min_agent_score = self.individualScore
        return

    def max_value(self, state, num_of_plys):
        if state.terminal_state(num_of_plys):
            return state.evaluate()
        best_value = None
        for next_state in state.successor("MAX"):
            next_state_min_value = self.min_value(next_state, num_of_plys + 1)
            if best_value is None:
                best_value = next_state_min_value
            best_value = self.otherAgent.utilityFunction(best_value, next_state_min_value)
        return best_value

    def min_value(self, state: State, num_of_plys):
        if state.terminal_state(num_of_plys):
            return state.evaluate()
        best_value = None
        for next_state in state.successor("MIN"):
            next_state_max_value = self.max_value(next_state, num_of_plys + 1)
            if best_value is None:
                best_value = next_state_max_value
            best_value = self.comparator(best_value, next_state_max_value)
        return best_value

    def miniMax(self, state: State):
        best_value = None
        best_edge = None
        num_of_plys = 0
        for next_state in state.successor("MIN"):
            value_of_new_state = self.max_value(next_state, num_of_plys + 1)
            current_edge = self.graph.get_edge(next_state.min_agent_current_location.prev, next_state.min_agent_current_location.successor)
            if best_value is None:
                best_value = value_of_new_state
                best_edge = current_edge
            elif not (best_value == self.utilityFunction(best_value, value_of_new_state)):
                best_value = value_of_new_state
                best_edge = current_edge
        return [best_edge[0], best_edge[1], best_edge[2]]

    def minimax_alpha_beta(self, state: State):
        best_edge = None
        num_of_plys = 0
        v = float('inf')
        alpha = float('-inf')
        beta = float('inf')
        for next_state in state.successor("MIN"):
            value_of_new_state = self.max_value_alpha_beta(next_state, num_of_plys + 1, alpha, beta)
            current_edge = self.graph.get_edge(next_state.min_agent_current_location.prev, next_state.min_agent_current_location.successor)
            if v > value_of_new_state:
                v = value_of_new_state
                best_edge = current_edge
            beta = min(v, beta)
        return [best_edge[0], best_edge[1], best_edge[2]]