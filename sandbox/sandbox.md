import heapq

open_set = []

heapq.heappush(open_set, (10, (1, 2, 3, 8, 4, 0, 7, 6, 5)))
heapq.heappush(open_set, (5, (1, 2, 3, 8, 0, 4, 7, 6, 5)))
heapq.heappush(open_set, (8, (1, 2, 3, 0, 8, 4, 7, 6, 5)))

f, current = heapq.heappop(open_set)

print(f)        # 5
print(current)  # (1, 2, 3, 8, 0, 4, 7, 6, 5)
