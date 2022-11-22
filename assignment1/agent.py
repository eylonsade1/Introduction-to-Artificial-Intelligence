
SCORE_MULTIPLYER = 1000

class Agent(object):
    def __init__(self, startingPosition):
        self.score = 0
        self.amountOfPeopleSaved = 0
        self.timeSpent = 0
        self.terminated = False
        self.state = None

    def calcualteScore(self):
        self.score = (self.amountOfPeopleSaved * SCORE_MULTIPLYER) - self.timeSpent

    def moveToPerform(self, observations):
        print ("not yet implemented for this agent")


class StupidGreedy(Agent):
    def __init__(self):
        super(StupidGreedy, self).__init__()
        print("stupid greedy constructor called")
    def moveToPerform(self, observations):
        return


class AIAgent(Agent):
    def __init__(self, h):
        self.heauristic = h