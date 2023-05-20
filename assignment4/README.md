# AI Assignment 4 - Decision-making under uncertainty

This repository contains the code and documentation for Assignment 4 of the course "Decision-making under uncertainty". The assignment focuses on solving the Hurricane Evacuation Problem using belief-state MDP (Markov Decision Process) and value iteration.

## Assignment Overview

The assignment is centered around the Hurricane Evacuation Problem, which involves making sequential decisions under uncertainty to evacuate people in a hurricane-affected area. The goal is to find an optimal policy that minimizes the expected time to save the people. The problem is an obscure variant of the Canadian traveler problem, where the locations of blockages are unknown but have a known probability of occurrence.

## Hurricane Evacuation Decision Problem - Domain Description

In this problem, you will be provided with a weighted undirected graph representing the hurricane-affected area. Each vertex has a known probability of being blocked, and these probabilities are jointly independent. The agent's actions are limited to traveling between vertices, and traversal times are determined by the weights of the edges. The start and target vertices are specified, and it is assumed that they are never blocked. The objective is to find a policy that saves the people in as short a time as possible (in expectation).

## Solution Method

To solve the Hurricane Evacuation problem, belief-state MDP and value iteration are used. The entire belief space is explicitly stored in memory and the value function is computed for the belief states. Additionally, the optimal action for each belief state is maintained during the value iteration to obtain the optimal policy at convergence.

The program reads the input data, including the graph and the start/target vertices. It constructs the belief space, initializes the value functions, and performs value iteration to compute the optimal policy. 

The program provides the following types of output:

1. Prints the value of each belief state and the optimal action, if it exists. Indicating if a state is irregular or unreachable.
2. Runs a sequence of simulations to evaluate the computed policy. Generates graph instances based on the blockage probabilities and simulate the agent's movement using the optimal policy. Then it Displays the graph instance and the sequence of actions. Allowing the user to run additional simulations with newly generated instances.


## Additional Information

For detailed formal instructions for this assignment, please refer to the file AIprogrammmingAssignment4.html.
