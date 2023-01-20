import itertools

from Graph import Graph
BLOCKED_PREFIX = "blockage_"
EVACUEE_PREFIX = "evacuee_"
MILD = "mild"
STORMY = "stromy"
EXTREME = "extreme"

class Node(object):
    def __init__(self, probabiliyTable, nodeName):
        self.name = nodeName
        self.table = probabiliyTable

    def get_name(self):
        return self.name

class WeatherNode(Node):
    def __init__(self, probabiliyTable):
        super(WeatherNode, self).__init__(probabiliyTable, "WeatherNode")
        self.legalValues = [MILD, STORMY, EXTREME]

    def __str__(self):
        str_weather = "WEATHER:\n"
        str_weather += "P(mild) = " + str(self.table[0]) + "\n"
        str_weather += "P(stormy) = " + str(self.table[1]) + "\n"
        str_weather += "P(extreme) = " + str(self.table[2]) + "\n"
        return str_weather


class BlockageNode(Node):
    def __init__(self, probabiliyTable, nodeName):
        super(BlockageNode, self).__init__(probabiliyTable, nodeName)
        self.legalValues = [True, False]

    def __str__(self):
        str_vertex = ""
        str_vertex += "P(Blocked|Mild) = " + str(self.table[0]) + "\n"
        str_vertex += "P(Blocked|Stormy) = " + str(self.table[1]) + "\n"
        str_vertex += "P(Blocked|Extreme) = " + str(self.table[2]) + "\n"
        return str_vertex

    def get_name(self):
        return self.name.split(BLOCKED_PREFIX)[1]

class EvacueeNode(Node):
    def __init__(self, neighobrs, nodeName):
        table = self.generateProbabiliyTable(neighobrs, nodeName)
        super(EvacueeNode, self).__init__(table, nodeName)
        self.legalValues = [True, False]

    def __str__(self):
        str_vertex = ""
        for permutation, value in self.table:
            str_vertex += "P(Evacuees| " + self.permutation_str(permutation) + ") = " + str(value) + "\n"
        return str_vertex

    def get_name(self):
        return self.name.split(EVACUEE_PREFIX)[1]

    def permutation_str(self, permutation):
        str_permutation = ""
        for vertex, value in permutation.items():
            if value:
                str_permutation += "Blockage" + vertex[2:] + ", "
            else:
                str_permutation += "not Blockage " + vertex[2:] + ", "
        return str_permutation[0:-2]


    def generateProbabiliyTable(self, neighborVertexes: list, nodeName):
        graph = Graph()

        def all_false_but_one(list_of_values):
            if 1 == sum(list_of_values):
                return True
            return False

        def new_row_values(neighbors, permut):
            row = dict()
            for ind in range(len(neighbors)):
                row[neighbors[ind][0].name] = permut[ind]
            return row

        def get_value(neighbor_name):
            for vert, val in false_table:
                if all_false_but_one(list(vert.values())) and vert[neighbor_name]:
                    return val
            print("In generate probability table method - this case shouldn't happen")

        nodeName = nodeName.split(EVACUEE_PREFIX)[1]
        this_is_me = graph.getVertexByName(nodeName)
        neighborVertexes.append((this_is_me, nodeName[2]))
        false_table = []
        length = len(neighborVertexes)
        all_permutations = list(itertools.product([True, False], repeat=length))
        for_second_round = []
        for permutation in all_permutations:
            new_row = new_row_values(neighborVertexes, permutation)
            if new_row[nodeName] and all_false_but_one(permutation):
                probability = graph.p2
                false_table.append((new_row, probability))
            elif not new_row[nodeName] and all_false_but_one(permutation):
                for vertex, value in new_row.items():
                    if value:
                        weight = graph.getEdgeWeigtFromVerName(nodeName, vertex)
                        probability = min(1, graph.p1*weight)
                        false_table.append((new_row, probability))
                        break
            else:
                for_second_round.append(new_row)

        for row in for_second_round:
            probability = 1.0
            for vertex, value in row.items():
                if value:
                    probability *= get_value(vertex)
            probability = round(probability, 2)
            false_table.append((row,probability))
        true_table = []
        for permutation, probability in false_table:
            new_probability = 1.0 - probability
            new_probability = round(new_probability, 2)
            true_table.append((permutation, new_probability))
        return true_table
