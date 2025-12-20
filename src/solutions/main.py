from math import inf
from typing import List
from utils import Item 
from brute_force_CHP import solve
# from brute_force_JAT import solve
# from efficient import solve

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
    [], 
    [],
    []
]

solution = solve(n, d, t_max, c_max, k_0, k_min, items_by_port)
print(solution) # 4

n: int = 3
d: List[List[float]] = [
    [0, 1, 3],
    [1, 0, 2],
    [3, 2, 0]
]
t_max: float = 1
c_max: float = 2
k_0: float = 6
k_min: float = 1
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
c_max: float = 1
k_0: float = 6
k_min: float = 1
items_by_port: List[List[Item]] = [
    [Item(2, 4, 3), Item(float(inf), float(inf), float(-inf))], 
    [Item(3, 6, 5), Item(2, 3, 3)],
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
k_0: float = 1
k_min: float = 0
items_by_port: List[List[Item]] = [
    [Item(2, 4, 3), Item(float(inf), float(inf), float(-inf))], 
    [Item(3, 6, 5), Item(1, 3, 3)],
    [Item(float(inf), float(inf), float(-inf)), Item(5, 5, 4)]
]

solution = solve(n, d, t_max, c_max, k_0, k_min, items_by_port)
print(solution) # 1

n: int = 3
d: List[List[float]] = [
    [0, 1, 3],
    [1, 0, 2],
    [3, 2, 0]
]
t_max: float = 6
c_max: float = 2
k_0: float = 2
k_min: float = 5
items_by_port: List[List[Item]] = [
    [Item(2, 4, 3), Item(float(inf), float(inf), float(-inf))], 
    [Item(3, 6, 5), Item(1, 3, 3)],
    [Item(float(inf), float(inf), float(-inf)), Item(5, 5, 4)]
]

solution = solve(n, d, t_max, c_max, k_0, k_min, items_by_port)
print(solution) # 2

n = 3
# m = 4 tipos de mercancías por puerto

d: List[List[float]] = [
    [0.0, 65.0, 41.3],
    [65.0, 0.0, 24.9],
    [41.3, 24.9, 0.0],
]

t_max: float = 250.4
c_max: float = 6.4
k_0: float = 11.1
k_min: float = 3.0

# Lista de 3 listas, cada una con 4 ítems
items_by_port: List[List[Item]] = [
    [Item(2.0, 12.9, 9.0), Item(inf, inf, -inf), Item(inf, inf, -inf), Item(1.8, 4.4, 3.6)],
    [Item(1.5, 7.9, 6.7), Item(1.5, 4.4, 3.7), Item(1.0, 14.1, 12.2), Item(1.4, 16.5, 15.8)],
    [Item(inf, inf, -inf), Item(1.9, 14.0, 12.6), Item(2.3, 14.8, 14.1), Item(inf, inf, -inf)],
]

solution = solve(n, d, t_max, c_max, k_0, k_min, items_by_port)
print(solution) # 22.799999999999997