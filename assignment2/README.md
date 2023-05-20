# AI Assignment 2 - Introduction to Artificial Intelligence

This repository contains the code and documentation for Assignment 2 of the course "Introduction to Artificial Intelligence." The assignment focuses on implementing cooperating and adversarial agents in the Hurricane Evacuation Problem.

## Assignment Overview

The assignment is centered around the Hurricane Evacuation Problem and involves implementing intelligent agents that aim to evacuate as many people as possible. The agents operate in a simplified version of the environment simulator introduced in Assignment 1. The assignment explores different game settings, ranging from cooperative to adversarial scenarios.

## Game Environment

The game environment consists of an undirected weighted graph, where all edge weights are assumed to be 1. Agents can perform two types of actions: "traverse" and "no-op". The semantics of these actions are the same as in Assignment 1. However, in this assignment, the agents take turns at every time unit rather than moving truly in parallel. The game ends when no more people can be saved or when a previously visited world state is revisited.

## Implementation Details

The implementation of this assignment involves the following steps:

1. The simulator queries the user about the parameters, including the type of game and other initialization parameters.

2. After the initialization, the simulator runs each agent in turn, obtaining the actions returned by the agents, and updating the world accordingly.

3. The simulator displays the world status after each step, including the state of the agents and their scores. The individual score (ISi) for each agent represents the number of people it has saved.

4. Each agent program, implemented as a function, follows a specific workflow. The simulator calls the agent with a set of observations, and the agent returns a move to be executed in the current world state. Agents are allowed to maintain internal state if needed. For this assignment, agents have access to the entire state of the world.

The assignment includes different types of games, each with its own objectives:

1. Adversarial (zero-sum game): Each agent aims to maximize its own individual score (number of people saved) minus the opposing agent's score. The agent's total score (TSi) is calculated as TS1 = IS1 - IS2 and TS2 = IS2 - IS1. Implement an "optimal" agent using mini-max with alpha-beta pruning for this type of game.

2. Semi-cooperative game: Each agent tries to maximize its own individual score, disregarding the other agent's score, except when breaking ties cooperatively. In this case, TS1 = IS1, breaking ties in favor of greater IS2.

3. Fully cooperative game: Both agents aim to maximize the sum of their individual scores, so TS1 = TS2 = IS1 + IS2.

To handle the large game tree, a cutoff mechanism and a heuristic static evaluation function are implemented. 

## Additional Information

For detailed formal instructions for this assignment, please refer to the file AIass2.html.
