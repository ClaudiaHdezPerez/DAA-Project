from math import inf
from typing import List
from utils import Item 
# from brute_force_CHP import solve
# from brute_force_JAT import solve
from efficient import solve

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
    [Item(3, 6, 5), Item(1, 3, 3)],
    [Item(float(inf), float(inf), float(-inf)), Item(5, 5, 4)]
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
    [Item(3, 6, 5), Item(1, 3, 3)],
    [Item(float(inf), float(inf), float(-inf)), Item(5, 5, 4)]
]

solution = solve(n, d, t_max, c_max, k_0, k_min, items_by_port)
print(solution) # 6

n: int = 3
d: List[List[float]] = [
    [0, 1, 3],
    [1, 0, 2],
    [3, 2, 0]
]
t_max: float = 6
c_max: float = 2
k_0: float = 4
k_min: float = 1
items_by_port: List[List[Item]] = [
    [Item(float(inf), float(inf), float(-inf)), Item(float(inf), float(inf), float(-inf))], 
    [Item(float(inf), float(inf), float(-inf)), Item(float(inf), float(inf), float(-inf))],
    [Item(float(inf), float(inf), float(-inf)), Item(float(inf), float(inf), float(-inf))]
]

solution = solve(n, d, t_max, c_max, k_0, k_min, items_by_port)
print(solution) # 4