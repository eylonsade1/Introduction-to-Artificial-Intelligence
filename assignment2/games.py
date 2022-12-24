import numpy as np
from Graph import Graph
from Agent import Agent
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


def min_value(self, state: s.State, num_of_plys, WORLD: Graph, agent: Agent):
    if state.terminal_state(num_of_plys):
        return state.evaluate()
    best_value = None
    for next_state in state.successor("MIN", WORLD):
        next_state_max_value = self.max_value(next_state, num_of_plys + 1, WORLD)
        if best_value is None:
            best_value = next_state_max_value
        if agent.type == 1:
            best_value = agent.other_agent.comparator(best_value, next_state_max_value)
        else:
            best_value = agent.comparator(best_value, next_state_max_value)
    return best_value


def max_value(self, state, num_of_plys, WORLD: Graph, agent: Agent):
    if state.terminal_state(num_of_plys):
        return state.evaluate()
    best_value = None
    for next_state in state.successor("MAX", WORLD):
        next_state_min_value = self.min_value(next_state, num_of_plys + 1, WORLD, agent)
        if best_value is None:
            best_value = next_state_min_value
        if agent.type == 1:
            best_value = agent.comparator(best_value, next_state_min_value)
        else:
            best_value = agent.other_agent.comparator(best_value, next_state_min_value)
    return best_value


def maxValueAlphaBeta(self, state, num_of_plys, graph: Graph, alpha, beta):
    if state.terminal_state(num_of_plys):
        # def evaluate_alpha_beta(self): return self.max_agent_score - self.min_agent_score
        return state.evaluate_alpha_beta()
    v = float('-inf')
    for next_state in state.successor("MAX", graph):
        v = max(v, self.minValueAlphaBeta(next_state, num_of_plys + 1, graph, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def minValueAlphaBeta(self, state: s.State, num_of_plys, graph: Graph, alpha, beta):
    if state.terminal_state(num_of_plys):
        return state.evaluate_alpha_beta()
    v = float('inf')
    for next_state in state.successor("MIN", graph):
        v = min(v, self.maxValueAlphaBeta(next_state, num_of_plys + 1, graph, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


def minimaxAlphaBeta(self, state:s.State, graph:Graph):
    best_edge = None
    num_of_plys = 0
    v = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    for next_state in state.successor("MAX", graph):
        value_of_new_state = self.minValueAlphaBeta(next_state, num_of_plys + 1, graph, alpha, beta)
        current_edge = graph.get_edge(next_state.max_agent_current_location.prev,next_state.max_agent_current_location.successor)
        if v < value_of_new_state:
            v = value_of_new_state
            best_edge = current_edge
        alpha = max(v, alpha)
    return [best_edge[0], best_edge[1], best_edge[2]]


def maximinAlphaBeta(self, state: s.State, graph: Graph):
    best_edge = None
    num_of_plys = 0
    v = float('inf')
    alpha = float('-inf')
    beta = float('inf')
    for next_state in state.successor("MIN", graph):
        value_of_new_state = self.maxValueAlphaBeta(next_state, num_of_plys + 1, graph, alpha, beta)
        current_edge = graph.get_edge(next_state.min_agent_current_location.prev, next_state.min_agent_current_location.successor)
        if v > value_of_new_state:
            v = value_of_new_state
            best_edge = current_edge
        beta = min(v, beta)
    return [best_edge[0], best_edge[1], best_edge[2]]


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
