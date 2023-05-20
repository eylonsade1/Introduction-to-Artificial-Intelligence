# AI Assignment 3 - Reasoning under Uncertainty

This repository contains the code and documentation for Assignment 3 of the course "Introduction to Artificial Intelligence." The assignment focuses on reasoning under uncertainty using Bayesian networks in the context of the Hurricane Evacuation Problem.

## Assignment Overview

The assignment revolves around the problem of reasoning under uncertainty in the Hurricane Evacuation Problem environment introduced in Assignment 1. It involves constructing a Bayesian network based on given parameters and performing probabilistic reasoning to answer specific questions related to blockages, evacuees, and weather conditions.

## Uncertain Hurricane Evacuation Problem - Domain Description

In this assignment, we consider a scenario where the blockages and evacuees in the environment are unknown, and there is uncertainty associated with their presence. The presence of blockages and evacuees at each vertex is modeled as a binary random variable. Additionally, a weather variable represents the weather conditions, which can be mild, stormy, or extreme.

The blockage events are assumed to be independent given the weather, with known distributions based on the weather conditions. The presence of evacuees is modeled using a noisy-or distribution, considering the blockages at neighboring vertices. The probabilities of blockages and evacuees are provided as parameters.

The assignment tasks involve reasoning about the likely locations of blockages, evacuees, and weather conditions given the evidence:

1. Determine the probability that each vertex contains evacuees.
2. Calculate the probability that each vertex is blocked.
3. Identify the distribution of the weather variable.
4. Compute the probability that a certain path (set of edges) is free from blockages.
5. (Bonus) Find the path from a given location to a goal that has the highest probability of being free from blockages.

## Requirements

The program should fulfill the following requirements:

### Part I: Bayesian Network Construction

- Read the input data, including the distribution parameters, from a file.
- Construct a Bayesian network based on the provided scenario.
- Output the constructed Bayesian network, including prior probabilities and conditional probabilities.

For example, the output for a given graph could be:

```
WEATHER:
  P(mild) = 0.1
  P(stormy) = 0.4
  P(extreme) = 0.5

VERTEX 1:
  P(blocked|mild) = 0.2
  P(blocked|stormy) = 0.4
  P(blocked|extreme) = 0.6

  P(Evacuees|Blockage 1, Blockage 2) = 0.94
  P(Evacuees|not Blockage 1, Blockage 2) = 0.8
  P(Evacuees|Blockage 1, not Blockage 2) = 0.7
  P(Evacuees|not Blockage 1, not Blockage 2) = 0

VERTEX 2:
...
```

### Part II: Probabilistic Reasoning

After constructing the Bayesian network, the program should support interactive operations involving evidence:

- Reset the evidence list to empty.
- Add a piece of evidence to the evidence list.
- Perform probabilistic reasoning to answer specific questions, such as probabilities of blockages, evacuees, and weather conditions.
- Report the results of the probabilistic reasoning, including all the posterior probabilities.
- Provide an option to quit the program.

Probabilistic reasoning can be done using various algorithms such as simple enumeration, variable elimination, polytree propagation, or sampling.

## Additional Information

For detailed formal instructions for this assignment, please refer to the file AI programmingAssignment3.html.
