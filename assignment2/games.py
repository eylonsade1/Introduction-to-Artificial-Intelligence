def maxSemiCooperative(bestVal, newState):
    if bestVal[0] < newState[0]:
        return newState
    if bestVal[0] == newState[0]:
        if bestVal[1] < newState[1]:
            return newState
    return bestVal


def minSemiCooperative(bestVal, newState):
    if bestVal[1] < newState[1]:
        return newState
    if bestVal[1] == newState[1]:
        if bestVal[0] < newState[0]:
            return newState
    return bestVal


def fullyCooperative(bestVal, newState):
    bestValSum = bestVal[0] + bestVal[1]
    newVal = newState[0] + newState[1]
    bestValMovements = bestVal[2]
    newStateMovements = newState[2]
    if bestValSum < newVal:
        return newState
    elif bestValSum == newVal and bestValMovements > newStateMovements:
        return newState
    return bestVal
