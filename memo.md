

What is the main point to solve N puzzle?
- heuristics

What should we need to think?
- 
- How many states
- 

@dataclass
class NumberBoardState:
    """The state of a single number board"""
    state: tuple[int]
    parent: State = None
    g: int = 0
    h: int = 0

    def get_state(self) -> tuple:
        return self.state

    def get_parent_state(self) -> State:
        return self.parent

    def get_f(self) -> int:
        return self.g + self.h

    def set_parent_state(self, new_parent: State) -> None:
        self.parent = new_parent
    
    def set_g(self, new_g: int) -> None:
        self.g = new_g
    
    def set_h(self, new_h: int) -> None:
        self.h = new_h

Opened-set
- total_selected_numbers: int = total_numbers selected in the opened set
- maximum_number: int = maximum number of states
- opened-set: min-heap = the states

print_parameter(current_state: opened-set: Opened-set)
1. print the maximun number of opend-set
2. print the order sequence of states in the shortest path
3. print the total numbers in opened-set
4. print the moving counts from start to end

init opend-set, closed-set with start
current = start

while (opend-set is not empty)
    if (curr_state == goal_state)
        print_parameter
        -> return
    calu h(current) -> get neighbor states in opened-set
        if
        - the states in closed-set doesn't exist
        - the g cost of thg state is lower than the state in closed set
    retrive & pop the lowest state in opened-set
        opened-set
        - maximum_number if maximum_number < len(opened-set)
        - total_number++
    if (neighbor(g) < current(g)>)
        current = neighbor
        closed-set.append(current)

print_error_report()

A -> B -> C -> D (f = g + h)
A -> F -> D (f = g + h)

op(A)
cl()
---
op(A) -> A
H()
-> B -> A
-> F -> A
op(B, F)
cl(A)
---
op(B, F) -> B
H()
-> E -> B -> A
-> G -> B -> A
-> C -> B -> A
-> F -> A
cl(A, B)
---
op(F, C, E, G) -> C
H()
-> F -> A
-> E -> B -> A
-> G -> B -> A
-> D -> C -> B -> A
-> H -> C -> B -> A
-> I -> C -> B -> A
-> J -> C -> B -> A
op(F, E, G, D, H, I, J)
cl(A, B, C)
---
op(F, E, G, D, H, I, J) -> D
H()
-> F -> A
-> E -> B -> A
-> G -> B -> A
-> H -> C -> B -> A
-> I -> C -> B -> A
-> J -> C -> B -> A
-> K -> D -> C -> B -> A 
op(F, E, G, H, I, J, K)
cl(A, B, C, D)

---
op(F, E, G, H, I, J, K) -> F
H()
-> E -> B -> A
-> G -> B -> A
-> C -> B -> A
-> D -> C -> B -> A
-> H -> C -> B -> A
-> I -> C -> B -> A
-> J -> C -> B -> A
-> K -> D -> C -> B -> A
-> D -> F -> A
-> L -> F -> A
-> K2 -> F -> A

Before
op(E, G, H, I, J, K)
    new_states(D, L, K2)
    for state in new_states
        if new_states in cl(A, B, C, D, F) 
        -> What happend??
        the g cost of D new state < current_state
        -> Update
            - parent node (current_state.set_paretnt_node(new_D.get_parent_node()))
            - g cost, h cost (current_state.set_paretnt_node(new_D.get_parent_node()))
Problem
- the child node of the parent node can't update when parent node update the parent of parent node
-> init shortest path

After
shortest_path(A -> B -> C -> D (f = g + h))
op(E, G, H, I, J, K)
    new_states(D, L, K2)
    for state in new_states
        if new_states in cl(A, B, C, D, F) 
        -> What happend??
        the g cost of D new state < current_state
        -> Update
            - shortest_path (update nodes?? I worry about time complexity. because )
            - g cost, h cost (current_state.set_paretnt_node(new_D.get_parent_node()))

Problem
- I worry about caltulating the shortest path of time. because it need to calculate the size of shortest path every time when the g cost of new state is lower than current state. for example node -> parent node -> parent node

---
op(E, G, H, I, J, K, L)
opened-set(A)
closed-set(A, B, C, D)

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


2026/10/31
- What's the difference between min-heap and priority queue?
- How do the program work if neigher state exists already in closed-set.
- When do the program update the parent state?

2026/10/22
- How are the elements orgnaized and maintained?
list, heap