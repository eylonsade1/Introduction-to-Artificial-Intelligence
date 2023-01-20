STORMY_MUL_FACTOR = 2
EXTREME_MUL_FACTOR = 3

class Vertex(object):
    def __init__(self, name, blockageProbability = 0):
        self.name = name
        self.mildBlockageProbability = blockageProbability

    def __str__(self):
        return "[{}:--blockedProbability:{}]\n".format(self.name, self.mildBlockageProbability)

    def getStormyProbabilty(self):
        stormyProb = round(self.mildBlockageProbability * STORMY_MUL_FACTOR, 2)
        return min(stormyProb, 1)

    def getExtremeProbability(self):
        extremePRob = round(self.mildBlockageProbability * EXTREME_MUL_FACTOR, 2)
        return min(extremePRob, 1)

    def getMildProbabilty(self):
        mildProb = round(self.mildBlockageProbability, 2)
        return min(mildProb, 1)

    def getProbabilityTable(self):
        return [self.getMildProbabilty(), self.getStormyProbabilty(), self.getExtremeProbability()]