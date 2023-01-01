class Weather(object):
    def __init__(self, mildProbability, stormyProbability, extremeProbability):
        if mildProbability + stormyProbability + extremeProbability == 1:
            self.mildProb = mildProbability
            self.stormyProb = stormyProbability
            self.extremeProb = extremeProbability
        else:
            raise Exception("Probability sum does not equal 1 - incorrect behavior")