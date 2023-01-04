from Graph import Graph
from BayesNetwork import BayesNetwork
import time
import utils

class Assignment3(object):
    def __init__(self):
        self.graph = Graph()
        self.bayesNetwork = BayesNetwork()

    def enumerateAsk(self, queryVariables, bayesianNetwork, evidenceVars = None):
        if evidenceVars == None:
            evidenceVars = []
        orderVarsFromNetwork = self.getVarsOrdered(bayesianNetwork)
        queryDistribution = [0 for _ in range(len(queryVariables.possibleVals))]
        for queryVal in queryVariables:
            extendedEvidenceVar = evidenceVars.append(queryVal)
            queryDistribution[queryVal] = self.enumerateAll(orderVarsFromNetwork, extendedEvidenceVar)
        normalizedQueryDistribution = self.normalize(queryDistribution)
        return normalizedQueryDistribution


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

    #todo represent baysian network object - generate order by parents
    def getVarsOrdered(self, bayesianNetwork):
        return []
    #todo
    def normalize(self, queryDistribution):
        return queryDistribution
    #todo proba claculation
    def calcProb(self):
        return 0