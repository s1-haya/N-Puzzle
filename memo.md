

What is the main point to solve N puzzle?
- heuristics

What should we need to think?
- 
- How many states
- 



A* alogorithm
f(n) = g(n) + h(n)

f: Total numbers of state
g: The numbers of the actual cost from the start node to the current node
j: The numbers of the estimate cost from the current node to the goal node
n: node, or ceil

1 2 3
8 0 4
7 6 5

f1 -> 100 + 3
f2 -> 100 + 2
f3 -> 100 + 4

We should choice the lowest state


Open-set
-> How should we orgnaize this data? heapq in Python

Closed-set
-> set


2026/10/22
- How are the elements orgnaized and maintained?
list, heap