import itertools

import Nodes
from Graph import Graph
from BayesNetwork import BayesNetwork
import out
import time
import utils
import numpy as np
BLOCKED_PREFIX = "blockage_"
EVACUEE_PREFIX = "evacuee_"
MILD = "mild"
STORMY = "stromy"
EXTREME = "extreme"

class Assignment3(object):
    def __init__(self):
        self.graph = Graph()
        self.bayesNetwork = BayesNetwork()

    def get_vals_from_evidence(self, x: Nodes, evidence: dict):
        for var, val in evidence:
            if var == x.name:
                return [val]
        return x.legalValues

    def enumerateAsk(self, queryVariable: list, evidenceVars = None):
        distribution = dict()
        possible_values = [self.get_vals_from_evidence(x, evidenceVars) for x in queryVariable]
        all_permutations = list(itertools.product(*possible_values))
        orderVarsFromNetwork = self.bayesNetwork.get_vars()
        for queryVal in all_permutations:
            extendedEvidenceVar = self.extend(evidenceVars,queryVal,0)
            distribution[queryVal] = self.enumerateAll(orderVarsFromNetwork, extendedEvidenceVar)
        normalizedQueryDistribution = self.normalize(distribution)
        return normalizedQueryDistribution

    def extend(self, s, var, val):
        """Copy dict s and extend it by setting var to val; return copy."""
        return {**s, var: val}

    def enumerateAll(self, variables, evidence):
        probability = 0
        if not variables:
            return 1.0
        variable = variables[1]
        if variable.value:
            probability = self.calcProb()
            probability = probability * self.enumerateAll(variables[:1], evidence)
        else:
            for possibleVal in variable.possibleVals:
                probability += probability * self.enumerateAll(variables[:1], evidence.append(possibleVal))

        return probability

    # def enumeration_ask(self, variable, evidence):
    #     """
    #     [Figure 14.9]
    #     Return the conditional probability distribution of variable X
    #     given evidence e, from BayesNet bn.
    #     'False: 0.716, True: 0.284'"""
    #     if variable.name in evidence.keys():
    #         return evidence[variable.name]
    #     distribution = dict()
    #     for xi in variable.legalValues:
    #         distribution[xi] = self.enumerate_all(self.bayesNetwork.get_vars(), self.extend(evidence, variable, xi))
    #     return self.normalize(distribution)


    # def enumerate_all(self, variables, evidence):
    #     """Return the sum of those entries in P(variables | e{others})
    #     consistent with e, where P is the joint distribution represented
    #     by bn, and e{others} means e restricted to bn's other variables
    #     (the ones other than variables). Parents must precede children in variables."""
    #     if not variables:
    #         return 1.0
    #     Y, rest = variables[0], variables[1:]
    #     Ynode = self.bayesNetwork.get_node(Y)
    #     if Y in evidence:
    #         return Ynode.p(evidence[Y], evidence) * self.enumerate_all(rest, evidence)
    #     else:
    #         return sum(Ynode.p(y, evidence) * self.enumerate_all(rest, self.extend(evidence, Y, y))
    #                    for y in Y.legalValues())

    # def getVarsOrdered(self, bayesianNetwork):
    #     return []
    # #todo
    def normalize(self, distribution):
        """Make sure the probabilities of all values sum to 1.
        Returns the normalized distribution.
        Raises a ZeroDivisionError if the sum of the values is 0."""
        total = sum(distribution.values())
        if not np.isclose(total, 1.0):
            for val in distribution:
                distribution[val] /= total
        return distribution
    #
    # #todo proba claculation
    # def calcProb(self):
    #     return 0

    def second_part_impl(self):
        evidence = dict()
        while True:
            menu = "Choose the action: \n1. Add evidence \n2. Reset evidence \n3. Probabilistic reasoning \n4. Exit\n"
            choice = int(input(menu))
            if choice == 1:
                evidence = self.add_evidence(evidence)
            elif choice == 2:
                evidence = dict()
                print("Evidence list cleared!\n")
            elif choice == 3:
                self.probabalistic_reasoning(evidence)
            elif choice == 4:
                break


    def userInit(self):
        self.partOne()
        self.second_part_impl()
            # #todo add evidence query
            # print("Not yet implemented")

    def partOne(self):
        print(self.bayesNetwork)

    def add_evidence(self, evidence):
        menu = "Choose the evidence type: \n1. Weather \n2. Blockage \n3. People\n"
        choice = int(input(menu))
        if choice == 1:
            weather_menu = "Choose the weather: \n1. Mild \n2. Stormy \n3. Extreme\n"
            weather = int(input(weather_menu))
            evidence["WeatherNode"] = MILD if weather == 1 else STORMY if weather == 2 else EXTREME
        elif choice == 2:
            node_menu = "Choose to which node you would like to add:"
            node_num = 1
            for node in self.graph.vertexes:
                node_menu += "\n" + str(node_num) + ". " + node.name
                node_num += 1
            node = int(input(node_menu + "\n"))
            evidence_menu = "Choose the evidence: \n1. blocked \n2. not blocked\n"
            evidence_choice = int(input(evidence_menu))
            evidence[BLOCKED_PREFIX + "#V" + str(node)] = "1" if evidence_choice == 1 else "0"
        elif choice == 3:
            node_menu = "Choose to which node you would like to add:"
            node_num = 1
            for node in self.graph.vertexes:
                    node_menu += "\n" + str(node_num) + ". " + node.name
                    node_num += 1
            node = int(input(node_menu + "\n"))
            evidence_menu = "Choose the evidence: \n1. people \n2. no people\n"
            evidence_choice = int(input(evidence_menu))
            evidence[EVACUEE_PREFIX + "#V" + str(node)] = "1" if evidence_choice == 1 else "0"

        return evidence

    def probabalistic_reasoning(self, evidence):
        while True:
            reasoning_menu = "Choose one of the following options: \n1. What is the probability that each of the vertices contains evacuees? \n2. What is the probability that each of the vertices is blocked? \n3. What is the distribution of the weather variable? \n4. What is the probability that a certain path (set of edges) is free from blockages? \n5. Return\n"
            choice = int(input(reasoning_menu))
            if choice == 1:
                nodes = []
                while True:
                    node_menu = "Choose node:"
                    node_menu = "Choose node:"
                    node_num = 1
                    for node in self.graph.vertexes:
                        node_menu += "\n" + str(node_num) + ". " + node.name
                        node_num += 1
                    node = int(input(node_menu))
                    node_menu += "\n" + str(node_num) + ". Start calc\n"
                    node = int(input(node_menu))
                    if node == node_num:
                        break
                    node = self.bayesNetwork.get_node(EVACUEE_PREFIX + "#V" + str(node))
                    nodes.append(node)
                nodes = [self.bayesNetwork.get_node(node) for node in nodes]
                probability = self.enumerateAsk(nodes, evidence)
                print('The probability is: ', probability)
            elif choice == 2:
                nodes = []
                while True:
                    node_menu = "Choose node:"
                    node_num = 1
                    for node in self.graph.vertexes:
                        node_menu += "\n" + str(node_num) + ". " + node.name
                        node_num += 1
                    node_menu += "\n" + str(node_num) + ". Start calc\n"
                    node = int(input(node_menu))
                    if node == node_num:
                        break
                    node = self.bayesNetwork.get_node(BLOCKED_PREFIX + "#V" + str(node))
                    nodes.append(node)
                nodes = [self.bayesNetwork.get_node(node) for node in nodes]
                probability = self.enumerateAsk(nodes, evidence)
                print('The probability is: ', probability)
            elif choice == 3:
                distribution = self.enumerateAsk([self.bayesNetwork.weatherNode], evidence)
                print('The distribution is: ', distribution)
            elif choice == 4:
                edges = []
                while True:
                    edge_menu = "Choose edge:"
                    edge_num = 1
                    for edge in self.graph.edges:
                        edge_menu += "\n" + str(edge_num) + ". " + edge.name
                        edge_num += 1
                    edge_menu += "\n" + str(edge_num) + ". Start calc\n"
                    edge = input(edge_menu)
                    if int(edge) == edge_num:
                        break
                    edges.append(self.graph.get_edge_by_name('#E' + edge))
                nodes = self.graph.get_vertex_list_from_edges(edges)
                nodes = [self.bayesNetwork.get_node(BLOCKED_PREFIX + node) for node in nodes]
                probability = self.enumerateAsk(nodes, evidence)
                print('The probability is: ', probability)
            elif choice == 5:
                break
