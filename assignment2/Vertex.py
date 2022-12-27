class Vertex(object):
    def __init__(self, name, numberOfPersons:int , isBrittle = False, isBlocked = False):
        self.name = name
        self.persons = int(numberOfPersons) #todo check if casting for int required
        self.isBrittle = isBrittle
        self.isBlocked = isBlocked

    def __str__(self):
        return "[{}:persons:{}--brittle:{}]\n".format(self.name, self.persons, self.isBrittle)

    def numOfPeople(self):
        return self.persons

class VertexWrapper(object):
    def __init__(self, state, parentWraper, accumelatedweight):
        self.state = state
        self.parentWraper = parentWraper
        self.accumelatedweight = accumelatedweight

    def __str__(self):
        return self.state.currentVertex.__str__()
