import numpy as np
from Graph import Graph
from Agent import Agent
from State import State
# def alpha_beta_search(state, game):
#     """Search game to determine best action; use alpha-beta pruning.
#     As in [Figure 5.7], this version searches all the way to the leaves."""
#
#     player = game.to_move(state)
#
#     # Functions used by alpha_beta
#     def max_value(state, alpha, beta):
#         if game.terminal_test(state):
#             return game.utility(state, player)
#         v = -np.inf
#         for a in game.actions(state):
#             v = max(v, min_value(game.result(state, a), alpha, beta))
#             if v >= beta:
#                 return v
#             alpha = max(alpha, v)
#         return v
#
#     def min_value(state, alpha, beta):
#         if game.terminal_test(state):
#             return game.utility(state, player)
#         v = np.inf
#         for a in game.actions(state):
#             v = min(v, max_value(game.result(state, a), alpha, beta))
#             if v <= alpha:
#                 return v
#             beta = min(beta, v)
#         return v
#
#     # Body of alpha_beta_search:
#     best_score = -np.inf
#     beta = np.inf
#     best_action = None
#     for a in game.actions(state):
#         v = min_value(game.result(state, a), best_score, beta)
#         if v > best_score:
#             best_score = v
#             best_action = a
#     return best_action


def minVal(state: State, numOfPlys, graph: Graph, agent: Agent):
    #if agent.terminal_state(numOfPlys):
    if agent.terminal_state():
        return state.evaluate()
    bestVal = None
    for nextState in state.successor("MIN", graph):
        nextStateMaxVal = maxVal(nextState, numOfPlys + 1, graph, agent)
        if bestVal is None:
            bestVal = nextStateMaxVal
        if agent.type == 1:
            bestVal = agent.other_agent.utilityFunction(bestVal, nextStateMaxVal)
        else:
            bestVal = agent.utilityFunction(bestVal, nextStateMaxVal)
    return bestVal


def maxVal(state, numOfPlys, graph: Graph, agent: Agent):
    #if agent.terminal_state(numOfPlys):
    if agent.terminal_state():
        return state.evaluate()
    bestVal = None
    for nextState in state.successor("MAX", graph):
        nextStateMinVal = minVal(nextState, numOfPlys + 1, graph, agent)
        if bestVal is None:
            bestVal = nextStateMinVal
        if agent.type == 1:
            bestVal = agent.utilityFunction(bestVal, nextStateMinVal)
        else:
            bestVal = agent.other_agent.utilityFunction(bestVal, nextStateMinVal)
    return bestVal


def maxValueAlphaBeta(state, numOfPlys, graph: Graph, alpha, beta, agent):
    #if agent.terminal_state(numOfPlys):
    if agent.terminal_state():
        # def evaluate_alpha_beta(self): return self.max_agent_score - self.min_agent_score
        return state.evaluate_alpha_beta()
    v = float('-inf')
    for nextState in state.successor("MAX", graph):
        v = max(v, minValueAlphaBeta(nextState, numOfPlys + 1, graph, alpha, beta, agent))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def minValueAlphaBeta(state: State, numOfPlys, graph: Graph, alpha, beta, agent):
    #if agent.terminal_state(numOfPlys):
    if agent.terminal_state():
        return state.evaluate_alpha_beta()
    v = float('inf')
    for nextState in state.successor("MIN", graph):
        v = min(v, maxValueAlphaBeta(nextState, numOfPlys + 1, graph, alpha, beta, agent))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


def minimaxAlphaBeta(state:State, graph:Graph, agent):
    bestEdge = None
    numOfPlys = 0
    if agent.type == 1:
        v = float('-inf')
        successor = state.successor("MAX", graph)
    else:
        v = float('inf')
        successor = state.successor("MIN", graph)
    alpha = float('-inf')
    beta = float('inf')
    for nextState in successor:
        if agent.type == 1:
            valOfNextState = minValueAlphaBeta(nextState, numOfPlys + 1, graph, alpha, beta, agent)
            currentEdge = graph.get_edge(nextState.max_agent_current_location.prev,nextState.max_agent_current_location.successor)
            if v < valOfNextState:
                v = valOfNextState
                bestEdge = currentEdge
            alpha = max(v, alpha)
        else:
            valOfNewState = maxValueAlphaBeta(nextState, numOfPlys + 1, graph, alpha, beta, agent)
            currentEdge = graph.get_edge(nextState.min_agent_current_location.prev, nextState.min_agent_current_location.successor)
            if v > valOfNewState:
                v = valOfNewState
                bestEdge = currentEdge
            beta = min(v, beta)
    return [bestEdge[0], bestEdge[1], bestEdge[2]]


# def maximinAlphaBeta(self, state: State, graph: Graph, agent):
#     bestEdge = None
#     numOfPlys = 0
#     v = float('inf')
#     alpha = float('-inf')
#     beta = float('inf')
#     for next_state in state.successor("MIN", graph):
#         valOfNewState = self.maxValueAlphaBeta(next_state, numOfPlys + 1, graph, alpha, beta, agent)
#         currentEdge = graph.get_edge(next_state.min_agent_current_location.prev, next_state.min_agent_current_location.successor)
#         if v > valOfNewState:
#             v = valOfNewState
#             bestEdge = currentEdge
#         beta = min(v, beta)
#     return [bestEdge[0], bestEdge[1], bestEdge[2]]


def minimax(state: State, graph: Graph, agent):
    bestVal = None
    bestEdge = None
    numOfPlys = 0
    if agent.type == 1:
        successor = state.successor("MAX", graph)
    else:
        successor = state.successor("MIN", graph)
    for nextState in successor:
        if agent.type == 1:
            valOfNewState = minVal(nextState, numOfPlys + 1, graph, agent)
            currentEdge = graph.get_edge(nextState.max_agent_current_location.prev, nextState.max_agent_current_location.successor)
        else:
            valOfNewState = maxVal(nextState, numOfPlys + 1, graph, agent)
            currentEdge = graph.get_edge(nextState.min_agent_current_location.prev, nextState.min_agent_current_location.successor)
        if bestVal is None:
            bestVal = valOfNewState
            bestEdge = currentEdge
        elif not (bestVal == agent.utilityFunction(bestVal, valOfNewState)):
            bestVal = valOfNewState
            bestEdge = currentEdge
    return [bestEdge[0], bestEdge[1], bestEdge[2]]


# def maximin(self, state: State, graph: Graph, agent):
#     bestVal = None
#     bestEdge = None
#     numOfPlys = 0
#     for nextState in state.successor("MIN", graph):
#         valOfNewState = self.maxVal(nextState, numOfPlys + 1, graph, agent)
#         currentEdge = graph.get_edge(nextState.min_agent_current_location.prev, nextState.min_agent_current_location.successor)
#         if bestVal is None:
#             bestVal = valOfNewState
#             bestEdge = currentEdge
#         elif not (bestVal == self.comparator(bestVal, valOfNewState)):
#             bestVal = valOfNewState
#             bestEdge = currentEdge
#     return [bestEdge[0], bestEdge[1], bestEdge[2]]


def query_player(game, state):
    """Make a move by querying standard input."""
    print("current state:")
    game.display(state)
    print("available moves: {}".format(game.actions(state)))
    print("")
    move = None
    if game.actions(state):
        move_string = input('Your move? ')
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('no legal moves: passing turn to next player')
    return move

# def alpha_beta_player(game, state):
#     return alpha_beta_search(state, game)

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


    def alpha_beta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
        """Search game to determine best action; use alpha-beta pruning.
        This version cuts off search and uses an evaluation function."""

        player = game.to_move(state)

        # Functions used by alpha_beta
        def max_value(state, alpha, beta, depth):
            if cutoff_test(state, depth):
                return eval_fn(state)
            v = -np.inf
            for a in game.actions(state):
                v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(state, alpha, beta, depth):
            if cutoff_test(state, depth):
                return eval_fn(state)
            v = np.inf
            for a in game.actions(state):
                v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        # Body of alpha_beta_cutoff_search starts here:
        # The default test cuts off at depth d or at a terminal state
        cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
        eval_fn = eval_fn or (lambda state: game.utility(state, player))
        best_score = -np.inf
        beta = np.inf
        best_action = None
        for a in game.actions(state):
            v = min_value(game.result(state, a), best_score, beta, 1)
            if v > best_score:
                best_score = v
                best_action = a
        return best_action


class UtilityFuncs:
    def maxSemiCooperative(self, bestVal, newState):
        if bestVal[0] < newState[0]:
            return newState
        if bestVal[0] == newState[0]:
            if bestVal[1] < newState[1]:
                return newState
        return bestVal

    def minSemiCooperative(self, bestVal, newState):
        if bestVal[1] < newState[1]:
            return newState
        if bestVal[1] == newState[1]:
            if bestVal[0] < newState[0]:
                return newState
        return bestVal

    def fullyCooperative(self, bestVal, newState):
        bestValSum = bestVal[0] + bestVal[1]
        newVal = newState[0] + newState[1]
        bestValMovements = bestVal[2]
        newStateMovements = newState[2]
        if bestValSum < newVal:
            return newState
        elif bestValSum == newVal and bestValMovements > newStateMovements:
            return newState
        return bestVal
