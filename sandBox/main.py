import os
from Assignment import Assignment1

if __name__ == '__main__':
    ass1 = Assignment1()
    ass1.createGraph(os.path.join(os.getcwd(), 'graph.csv'))
    ass1.userInit()
    # program

