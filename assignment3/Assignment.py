from Graph import Graph
from BayesNetwork import BayesNetwork
import out
import time
import utils

class Assignment3(object):
    def __init__(self):
        self.graph = Graph()
        self.bayesNetwork = BayesNetwork()

    def enumerateAsk(self, queryVariables, evidenceVars = None):
        if evidenceVars == None:
            evidenceVars = []
        orderVarsFromNetwork = self.getVarsOrdered(self.bayesNetwork)
        queryDistribution = [0 for _ in range(len(queryVariables.possibleVals))]
        for queryVal in queryVariables:
            extendedEvidenceVar = evidenceVars.append(queryVal)
            queryDistribution[queryVal] = self.enumerateAll(orderVarsFromNetwork, extendedEvidenceVar)
        normalizedQueryDistribution = self.normalize(queryDistribution)
        return normalizedQueryDistribution


    def enumerateAll(variables, evidence):
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

    # def getVarsOrdered(self, bayesianNetwork):
    #     return []
    # #todo
    # def normalize(self, queryDistribution):
    #     return queryDistribution
    #
    # #todo proba claculation
    # def calcProb(self):
    #     return 0

    def second_part_impl(self):
        evidence = dict()
        while True:
            menu = "Choose the action: \n1. Add evidence \n2. Reset evidence \n3. Probabilistic reasoning \n4. Exit"
            choice = int(input(menu))
            if choice == 1:
                evidence = self.add_evidence(evidence)
            elif choice == 2:
                evidence = dict()
                print("Evidence list cleared!")
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
            evidence["W"] = "1" if weather == 1 else "2" if weather == 2 else "3"
        elif choice == 2:
            node_menu = "Choose to which node you would like to add:"
            node_num = 1
            for node in self.graph.vertexes:
                node_menu += "\n" + str(node_num) + ". " + node.name
                node_num += 1
            node = int(input(node_menu + "\n"))
            evidence_menu = "Choose the evidence: \n1. blocked \n2. not blocked\n"
            evidence_choice = int(input(evidence_menu))
            evidence["B("+str(node)+")"] = "1" if evidence_choice == 1 else "0"
        elif choice == 3:
            node_menu = "Choose to which node you would like to add:"
            node_num = 1
            for node in self.graph.vertexes:
                    node_menu += "\n" + str(node_num) + ". " + node.name
                    node_num += 1
            node = int(input(node_menu + "\n"))
            evidence_menu = "Choose the evidence: \n1. people \n2. no people\n"
            evidence_choice = int(input(evidence_menu))
            evidence["Ev("+str(node)+")"] = "1" if evidence_choice == 1 else "0"

        return evidence

    def probabalistic_reasoning(self, evidence):
        while True:
            reasoning_menu = "Choose one of the following options: \n1. What is the probability that each of the vertices contains evacuees? \n2. What is the probability that each of the vertices is blocked? \n3. What is the distribution of the weather variable? \n4. What is the probability that a certain path (set of edges) is free from blockages? \n5. Return"
            choice = int(input(reasoning_menu))
            if choice == 1:
                node_menu = "Choose node:"
                node_num = 1
                for node in self.graph.vertexes:
                    node_menu += "\n" + str(node_num) + ". " + node.name
                    node_num += 1
                node = int(input(node_menu))
            elif choice == 2:
                node_menu = "Choose node:"
                node_num = 1
                for node in self.graph.vertexes:
                    node_menu += "\n" + str(node_num) + ". " + node.name
                    node_num += 1
                node = int(input(node_menu))
            elif choice == 3:
                distribution = self.enumerateAsk([self.bayesNetwork.weatherNode], evidence)
                print('->\tThe distribution is: ', distribution)
            elif choice == 4:
                edge_menu = "Choose edge:"
                edge_num = 1
                for edge in self.graph.edges:
                    edge_menu += "\n" + str(edge_num) + ". " + edge.name
                    edge_num += 1
                edge = int(input(edge_menu))
            elif choice == 5:
                break
