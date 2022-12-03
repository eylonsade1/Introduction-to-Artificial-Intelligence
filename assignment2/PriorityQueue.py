import sys

class PriorityQueue(object):

    def __init__(self, f):
        self.queue = []
        self.f = f

    def __str__(self):
        return ' '.join([i.__str__() for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0

    def insert(self, data):
        self.queue.append(data)

    def pop(self):
        heuristic_values = dict()
        if self.is_empty():
            return None
        min_element_index = 0
        min_value = self.f(self.queue[0])
        heuristic_values[self.queue[0]] = min_value
        min_element_amount_to_save = self.queue[0].state.currentVertex.persons
        for i in range(len(self.queue)):
            queue_i_res = self.f(self.queue[i])
            heuristic_values[self.queue[i]] = queue_i_res
            queue_i_amount_to_save = self.queue[i].state.currentVertex.persons
            if queue_i_res < min_value or (queue_i_res == min_value and queue_i_amount_to_save < min_element_amount_to_save) or (queue_i_res == min_value and queue_i_amount_to_save == min_element_amount_to_save and (int(self.queue[i].state.currentVertex.persons) > 0 and (not int(self.queue[min_element_index].state.currentVertex.persons) > 0))):
                min_element_index = i
                min_value = queue_i_res
                min_element_amount_to_save = queue_i_amount_to_save
        item = self.queue[min_element_index]
        del self.queue[min_element_index]
        return item
