from math import inf
from typing import List, Tuple
from  utils import Item, Merchandise


def solve(
    n: int,
    d: List[List[float]],                 # d[i][j] = d_{ij}
    t_max: float,                         # T_max
    c_max: float,                         # C_max
    k_0: float,                           # K_0
    k_min: float,                         # K_min
    items_by_port: List[List[Item]]       # M_i for each port i
) -> float:
    return _solve(
        n, d, t_max, c_max, k_0, k_min, 
        items_by_port, 0, k_0, [False for _ in range(n)],
        [], [[] for _ in range(n)]
    )

def _solve(
    n: int, d: List[List[float]], t_max: float,
    c_max: float, k_0: float, k_min: float,
    items_by_port: List[List[Item]],
    port_i: int, max_profit: float,
    visited: List[bool], route: List[int],
    l_i: List[List[Merchandise]]
) -> float:
    # If I stay in Amsterdam, finish the travel
    if port_i == 0 and visited[0]:
        route.append(0)
        print(route)
        max_profit = max(
            max_profit,
            _profit_by_route(
                c_max, k_0, k_min, items_by_port, 
                route, l_i, 0, max_profit
            ) 
        )
        route.pop() 
        return max_profit

    route.append(port_i)
    # Go to port j from port i
    for port_j in range(n):
        if port_i == port_j:
            continue
        
        if not visited[port_j] and (t_max - (d[port_i][port_j] + d[port_j][0])) >= 0:
            visited[port_j] = True
            max_profit = max(
                max_profit,
                _solve(
                    n, d, t_max - d[port_i][port_j], c_max, 
                    k_0, k_min, items_by_port, port_j,
                    max_profit, visited, route, l_i
                )
            )
            visited[port_j] = False
            
    route.pop()
            
    return max_profit

def _profit_by_route(
    c_max: float, k_0: float, k_min: float,
    items_by_port: List[List[Item]], route: List[int],
    l_i: List[List[Merchandise]], i: int, max_profit: float
) -> float:
    if k_0 < 0:
        return float(-inf)
    
    port = route[i]
    
    if i == len(route) - 1:
        return k_0 + _sell_all(l_i[port], items_by_port[port])
    
    for sell in _sell(l_i[port], items_by_port[port], [], 0, []):
        rest = [l for l in l_i[port] if l not in sell[0]]
        sold = [l for l in l_i[port] if l in sell[0]]
        capacities_sold = _calculate_weight(sold)
        for buy in _buy(port, items_by_port[port], [], 0, [], c_max + capacities_sold, k_0 + sell[1] - k_min):
            capacities_bought = _calculate_weight(buy[0])
            l_i[route[i+1]] = rest + buy[0]
            max_profit = max(
                max_profit, 
                _profit_by_route(
                    c_max + capacities_sold - capacities_bought, k_0 + sell[1] - k_min - buy[1],
                    k_min, items_by_port, route, l_i, i + 1, max_profit
                )
            )
    
    return max_profit

def _sell(
    goods: List[Merchandise],
    items_at_port: List[Item], 
    goods_sold: List[Merchandise],
    i: int,
    result: List[Tuple[List[Merchandise], int]]
) -> List[Tuple[List[Merchandise], int]]:
    if i == len(goods):
        sold = 0
        for j in goods_sold:
            sold += items_at_port[j.k].sell_price
            
        result.append((goods_sold.copy(), sold))
        return result
    
    merchandise = goods[i]
    goods_sold.append(merchandise)
    _sell(goods, items_at_port, goods_sold, i + 1, result)
    goods_sold.pop()
    _sell(goods, items_at_port, goods_sold, i + 1, result)
        
    return result

def _sell_all(goods: List[Merchandise], items_at_port: List[Item]) -> float:
    sold = 0
    for j in goods:
        sold += items_at_port[j.k].sell_price
    
    return sold

def _buy(
    port: int,
    items_at_port: List[Item], 
    goods_sold: List[Merchandise],
    i: int,
    result: List[Tuple[List[Merchandise], int]],
    c_max: float, 
    k: float
) -> List[Tuple[List[Merchandise], int]]:
    if i == len(items_at_port):
        sold = 0
        for j in goods_sold:
            sold += j.buy_price
            
        result.append((goods_sold.copy(), sold))
        return result
    
    merchandise = Merchandise(port, i, items_at_port[i].w, items_at_port[i].buy_price)
    if c_max - merchandise.w >= 0 and k - merchandise.buy_price >= 0:
        goods_sold.append(merchandise)
        _buy(port, items_at_port, goods_sold, i + 1, result, c_max - merchandise.w, k - merchandise.buy_price)
        goods_sold.pop()
    _buy(port, items_at_port, goods_sold, i + 1, result, c_max, k)
        
    return result

def _calculate_weight(goods: List[Merchandise]) -> float:
    peso = 0
    for item in goods:
        peso += item.w
        
    return peso