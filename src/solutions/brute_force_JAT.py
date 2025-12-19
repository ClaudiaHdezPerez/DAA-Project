from typing import List
from utils import Item, Merchandise


def solve(
    n: int,
    d: List[List[float]],                 # d[i][j] = d_{ij}
    t_max: float,                         # T_max
    c_max: float,                         # C_max
    k_0: float,                           # K_0
    k_min: float,                         # K_min
    items_by_port: List[List[Item]]       # M_i para cada puerto i
) -> float:
    ports_visited = [False] * n
    ports_visited[0] = True
    m = len(items_by_port[0])
    return max(k_0, buy(
        n, d, t_max, c_max, k_0, k_min, m,
        items_by_port, 0, [], ports_visited, 0
    ))

def sell(
    n: int, d: List[List[float]], t_max: float, c_max: float, k_0: float,
    k_min: float, size: int, items_by_port: List[List[Item]], port: int,
    items_on_board: List[Merchandise], ports_visited: list[bool], j: int
) -> float:
    purchase_gain = buy(
        n, d, t_max, c_max, k_0, k_min, size, items_by_port,
        port, items_on_board, ports_visited, 0
    )
    sell_gain = -1
    
    if j >= len(items_on_board):
        return purchase_gain
    
    if items_on_board:
        m = items_on_board.pop(j)
        sell_price = items_by_port[port][m.k].sell_price
        sell_gain = sell(
            n, d, t_max, c_max + m.w, k_0 + sell_price, k_min, size,
            items_by_port, port, items_on_board, ports_visited, j
        )
        items_on_board.insert(j, m)
        sell_gain = max(sell_gain, sell(
            n, d, t_max, c_max, k_0, k_min, size, items_by_port,
            port, items_on_board, ports_visited, j + 1
        ))
    
    return max(purchase_gain, sell_gain)

def buy(
    n: int, d: List[List[float]], t_max: float, c_max: float,
    k_0: float, k_min: float, size: int, items_by_port: List[List[Item]],
    port: int, items_on_board: List[Merchandise],
    ports_visited: list[bool], j: int
) -> float:
    travel_gain, purchase = k_0, -1
    
    if k_min > travel_gain:
        return -1
    
    travel_gain = travel(
        n, d, t_max, c_max, k_0 - k_min, k_min, size,
        items_by_port, port, items_on_board, ports_visited
    )
    
    if j >= size:
        return travel_gain
    
    current_item = items_by_port[port][j]
    funds = k_0 - current_item.buy_price
    capacity_left = c_max - current_item.w
    
    if k_min <= funds and capacity_left >= 0:
        items_on_board.append(Merchandise(
            i=port, k=j, w=current_item.w,
            buy_price=current_item.buy_price
        ))
        purchase = buy(
            n, d, t_max, capacity_left, funds, k_min,
            size, items_by_port, port, items_on_board, 
            ports_visited, j + 1
        )
        
        items_on_board.pop()
        
    purchase = max(purchase, buy(
        n, d, t_max, c_max, k_0, k_min,
        size, items_by_port, port, items_on_board, 
        ports_visited, j + 1
    ))
        
    return max(purchase, travel_gain)

def travel(
    n: int, d: List[List[float]], t_max: float, c_max: float,
    k_0: float, k_min: float, size: int, items_by_port: List[List[Item]],
    port: int, items_on_board: List[Merchandise], ports_visited: list[bool]
) -> float:
    
    final_gain = k_0 + sum([
        items_by_port[0][m.k].sell_price for m in items_on_board
    ])
    
    max_gain = -1
    
    for i in range(n):        
        if (ports_visited[i] and i > 0) or i == port:
            continue
        
        if t_max >= d[port][i] + d[i][0]:
            ports_visited[i] = True
            next_port_gain = sell(
                n, d, t_max - d[port][i], c_max, k_0, k_min, size,
                items_by_port, i, items_on_board, ports_visited, 0
            ) if i > 0 else final_gain
            max_gain = max(max_gain, next_port_gain)
            
            if i > 0:
                ports_visited[i] = False
            
    return max_gain