# AI Assignment 1 - Introduction to Artificial Intelligence

This repository contains the code and documentation for Assignment 1 of the course "Introduction to Artificial Intelligence." The assignment focuses on implementing an environment simulator and agents for the Hurricane Evacuation Problem.

## Assignment Overview

The assignment is divided into two parts:

### Part I: Simulator and Simple Agents

Part I involves implementing an environment simulator and several simple agents. The simulator is responsible for creating the environment based on a given weighted graph and other parameters. The simple agents include a human agent, a stupid greedy agent, and a saboteur agent. The simulator runs each agent in sequence and updates the state of the world according to their actions.

### Part II: Search Agents

Part II focuses on implementing intelligent search agents using different algorithms. The search agents assume that they are acting alone and aim to minimize the time required to collect all the people in the graph. The implemented search agents include a greedy search agent, an A* search agent, and a real-time A* search agent. The performance of these agents is evaluated based on the time taken to achieve the goal.

## Implementation Details

### Part I: Simulator and Simple Agents

- The implementation includes an environment simulator that reads a weighted graph and other parameters from a file. The simulator initializes the environment based on this input.
- A human agent is implemented, allowing manual input from the user for each move. This agent is useful for debugging and evaluation purposes.
- A stupid greedy agent is implemented, that computes and follows the shortest currently unblocked path to the next vertex with people to be rescued. This agent prioritizes efficiency in reaching the targets.
- A saboteur agent is created, which breaks brittle vertices by visiting them. The agent computes the shortest path to a brittle vertex and moves in that direction, disregarding people to be rescued.

### Part II: Search Agents

- The implementation involves intelligent search agents using different algorithms to minimize the time required to collect all the people in the graph.
- A greedy search agent is implemented, which selects the move with the best immediate heuristic value to expand next. This agent makes local optimization choices.
- An A* search agent is created, utilizing an admissible heuristic evaluation function to find the optimal path. This agent considers both the cost to reach a vertex and the estimated cost to the goal.
- A real-time A* search agent is implemented, which performs a user-determined number of expansions before each move decision. This agent balances the trade-off between computation time and path quality.


## Additional Information

For detailed formal instructions for this assignment, please refer to the file Alass1.html.
