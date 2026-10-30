# def create_openset(numbers: list(int)) -> list:
from heapq import heappush, heapify


def A_star(start: tuple, end: tuple) -> None:
    # display:
    # 

def main() -> None:
    heap = []
    numbers = [2, 3, 1, 5]
    heappush(heap, (2, "A"))
    heappush(heap, (4, "B"))
    heappush(heap, (5, "C"))
    print(heap[0])

    heapify(numbers)
    print(numbers[0])

if __name__ == '__main__' :
    main()

# # T: Goal State
# # C: Current State
# # S: Start State

# ---

# # f(n) = g(n) + h(n)
# # n: node
# # f: total cost
# # g: real cost from S to C
# # h: estimate cost from C to G

# ---
# # Heuristic Function
# -> to estiate the cost to move from C to G

# A* -> 500
# - H1
# - H2
# - H3


# def manhattan_distance()

#     p, q
#     p(x1, y1), q(x2, y2)
#     |x1 - x2| + |y1 - y2|
#     list[[1, 2], [2, 1]]
