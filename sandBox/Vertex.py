class Vertex(object):
    def __init__(self, name, numberOfPersons:int , isBrittle = False, isBlocked = False):
        self.name = name
        self.persons = numberOfPersons
        self.isBrittle = isBrittle
        self.isBlocked = isBlocked

    def __str__(self):
        return self.name