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

    def getVals(self, node: Nodes, evidence: dict):
        values = []
        if node in evidence.keys():
            values.append((node, evidence[node]))
            return [values]
        for legalVal in node.legalValues:
            values.append((node, legalVal))
        return values

    def enumerateAsk(self, queryVariable: list, evidenceVars=None):
        distribution = dict()
        possibleValues = []
        for variable in queryVariable:
            possibleValues.append(self.getVals(variable, evidenceVars))
        all_permutations = list(itertools.product(*possibleValues))
        orderVarsFromNetwork = self.bayesNetwork.get_vars()
        for queryVal in all_permutations:
            extendedEvidenceVar = self.extend(evidenceVars, queryVal)
            calculatedProbability = self.enumerateAll(orderVarsFromNetwork, extendedEvidenceVar)
            distribution[queryVal] = calculatedProbability
        normalizedQueryDistribution = self.normalize(distribution)
        return normalizedQueryDistribution

    def extend(self, s, var):
        return {**s, var[0][0]: var[0][1]}

    def enumerateAll(self, variables, evidence):
        if not variables:
            return 1.0
        Y = variables[0]
        value = evidence[Y] if Y in evidence.keys() else None
        # values = [(Y, evidence[Y])] if Y in evidence.keys() else [(Y, value) for value in Y.legalValues]
        parents = self.bayesNetwork.getParents(Y)
        parent_evidence = dict()
        for parent in parents:
            if parent in evidence.keys():
                parent_evidence[parent] = evidence[parent]
        if value is not None:
            value_probability = Y.getProbabilityWithParents(value, parent_evidence)
            # print(value_probability) for debugging purposes
            recurssionValue = self.enumerateAll(variables[1:], evidence)
            # print("{} * {}".format(value_probability, recurssionValue))
            return value_probability * recurssionValue
        else:
            probability = 0
            for YLegalvalue in Y.legalValues:
                value_probability = Y.getProbabilityWithParents(YLegalvalue, parent_evidence)
                evidence[Y] = YLegalvalue
                if value_probability:
                    probability += (value_probability * self.enumerateAll(variables[1:], evidence))
            return probability

    # #todo
    def normalize(self, distribution):
        total = sum(distribution.values())
        if total == 0:
            return 0
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
            nodeObj = self.bayesNetwork.get_node("WeatherNode")
            evidence[nodeObj] = MILD if weather == 1 else STORMY if weather == 2 else EXTREME
        elif choice == 2:
            node_menu = "Choose to which node you would like to add:"
            node_num = 1
            for node in self.graph.vertexes:
                node_menu += "\n" + str(node_num) + ". " + node.name
                node_num += 1
            node = int(input(node_menu + "\n"))
            evidence_menu = "Choose the evidence: \n1. blocked \n2. not blocked\n"
            evidence_choice = int(input(evidence_menu))
            nodeObj = self.bayesNetwork.get_node(BLOCKED_PREFIX + "#V" + str(node))
            evidence[nodeObj] = True if evidence_choice == 1 else False
        elif choice == 3:
            node_menu = "Choose to which node you would like to add:"
            node_num = 1
            for node in self.graph.vertexes:
                node_menu += "\n" + str(node_num) + ". " + node.name
                node_num += 1
            node = int(input(node_menu + "\n"))
            evidence_menu = "Choose the evidence: \n1. people \n2. no people\n"
            evidence_choice = int(input(evidence_menu))
            nodeObj = self.bayesNetwork.get_node(EVACUEE_PREFIX + "#V" + str(node))
            evidence[nodeObj] = True if evidence_choice == 1 else False

        return evidence

    def generateString(self, probabilityStruct):
        stringOfProbability = ""
        try:
            for key, value in probabilityStruct.items():
                for nodeAss in key:
                    stringOfProbability += "{}:{}, ".format(nodeAss[0].name, nodeAss[1])
                stringOfProbability += "= {}\n".format(round(value, 2))
            return stringOfProbability
        except Exception:
            print("Failed on generating comfortable string from probabilityStructure- returning objects")
            return probabilityStruct

    def probabalistic_reasoning(self, evidence):
        while True:
            reasoning_menu = "Choose one of the following options: \n1. What is the probability that each of the vertices contains evacuees? \n2. What is the probability that each of the vertices is blocked? \n3. What is the distribution of the weather variable? \n4. What is the probability that a certain path (set of edges) is free from blockages? \n5. Return\n"
            choice = int(input(reasoning_menu))
            if choice == 1:
                nodes = []
                node_menu = "Choose node:"
                node_num = 1
                for node in self.graph.vertexes:
                    node_menu += "\n" + str(node_num) + ". " + node.name
                    node_num += 1
                node_menu += "\n" + str(node_num) + ". Start calc\n"
                while True:
                    node = int(input(node_menu))
                    if node == node_num:
                        break
                    node = self.bayesNetwork.get_node(EVACUEE_PREFIX + "#V" + str(node))
                    if node not in nodes:
                        nodes.append(node)
                probability = self.enumerateAsk(nodes, evidence)
                stringProbability = self.generateString(probability)
                print('probability:\n ', stringProbability)
            elif choice == 2:
                nodes = []
                node_menu = "Choose node:"
                node_num = 1
                for node in self.graph.vertexes:
                    node_menu += "\n" + str(node_num) + ". " + node.name
                    node_num += 1
                node_menu += "\n" + str(node_num) + ". Start calc\n"
                while True:
                    node = int(input(node_menu))
                    if node == node_num:
                        break
                    node = self.bayesNetwork.get_node(BLOCKED_PREFIX + "#V" + str(node))
                    if node not in nodes:
                        nodes.append(node)
                probability = self.enumerateAsk(nodes, evidence)
                stringProbability = self.generateString(probability)
                print('probability:\n ', stringProbability)
            elif choice == 3:
                distribution = self.enumerateAsk([self.bayesNetwork.weatherNode], evidence)
                stringProbability = self.generateString(distribution)
                print('distribution: ', stringProbability)
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
                stringProbability = self.generateString(probability)
                print('probability:\n ', stringProbability)
            elif choice == 5:
                break
