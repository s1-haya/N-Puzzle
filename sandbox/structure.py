from heapq import heappush, heapify
from dataclasses import dataclass, field


@dataclass
class NumberBoardState:
    """The state of a single number board"""
    state: tuple
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




# Open-Set
# Closed-set

# F = G + H
# Each state have F, G, H
# State has a previous state
# ex) 
# - stateA(start) -> stateB -> stateC(goal)
# stateC(goal) has stateB
# stateB has stateA(start)
# status
# - start
# - end
# - normal

def astar(start: tuple, goal: tuple) -> None:
    print(start)

def main() -> None:
    # 1. Validate Input File
    # 2. Check whther this number board pass
    # 3. Solve the puzzle number board using A*
    # 3.1 init opened-set, closed-set
    goal: tuple = (1, 2, 3, 8, 0, 4, 7, 6, 5)
    number_board: tuple = (1, 2, 3, 8, 0, 4, 7, 6, 5)
    stateA = NumberBoardState(number_board)
    stateA.set_g(3)
    stateA.set_h(3)
    stateB = NumberBoardState(number_board)
    stateB.set_g(2)
    stateB.set_h(2)
    
    opened_set: list[NumberBoardState] = []   
    heappush(opened_set, (stateA.get_f(), stateA))
    heappush(opened_set, (stateB.get_f(), stateB))

    print(opened_set)
    closed_set: set[NumberBoardState] = {}
    if stateA.get_state() == goal:
        print(True)
    else:
        print(False)
    print(stateA)

    # 4. Print 4 parameters
    # - Total numbers of states in opened list set
    # - Maximum number of states during search
    # - The ordered sequence of states that make up the soultion
    # - if the puzzle is unsolable, it need to inform the user and exit

if __name__ == '__main__':
    main()
