class Vertex(object):
    def __init__(self, name, isGoal =False , isStart = False, brokenProb = 0):
        self.name = name
        self.isGoal = isGoal
        self.isStart = isStart
        self.brokenProb = brokenProb

    def __str__(self):
        return "[{}:is start:{}--is goal:{} -- probability of being broken:{}]\n".format(self.name, self.isStart,
                                                                                         self.isGoal, self.brokenProb)
    def setIsStart(self, isStart):
        self.isStart = isStart

    def setIsGoal(self, isGoal):
        self.isGoal = isGoal

    def setBrokenProb(self, probability):
        self.brokenProb = float(probability)
