from math import inf
# from brute_force_CHP import solve, List, Item
from brute_force_JAT import solve, List, Item

n: int = 3
d: List[List[float]] = [
    [0, 1, 3],
    [1, 0, 2],
    [3, 2, 0]
]
t_max: float = 2
c_max: float = 2
k_0: float = 5
k_min: float = 1
items_by_port: List[List[Item]] = [
    [Item(2, 4, 3), Item(float(inf), float(inf), float(-inf))], 
    [Item(3, 2, 6), Item(1, 3, 3)],
    [Item(float(inf), float(inf), float(-inf)), Item(5, 1, 5)]
]

solution = solve(n, d, t_max, c_max, k_0, k_min, items_by_port)
print(solution) # 5

n: int = 3
d: List[List[float]] = [
    [0, 1, 3],
    [1, 0, 2],
    [3, 2, 0]
]
t_max: float = 6
c_max: float = 2
k_0: float = 4
k_min: float = 0
items_by_port: List[List[Item]] = [
    [Item(2, 4, 3), Item(float(inf), float(inf), float(-inf))], 
    [Item(3, 2, 6), Item(1, 3, 3)],
    [Item(float(inf), float(inf), float(-inf)), Item(5, 1, 5)]
]

solution = solve(n, d, t_max, c_max, k_0, k_min, items_by_port)
print(solution) # 8