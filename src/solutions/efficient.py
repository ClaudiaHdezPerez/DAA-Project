import math
import random
from typing import List, Set, Optional
from utils import Item, Merchandise


# Clase para representar el estado
class State:
    def __init__(self, current_port: int = 0, capital: float = 0.0, 
                 time: float = 0.0, used_capacity: float = 0.0,
                 route: List[int] = None, inventory: List[Merchandise] = None):
        self.current_port = current_port
        self.capital = capital
        self.time = time
        self.used_capacity = used_capacity
        self.route = route if route is not None else []
        self.inventory = inventory if inventory is not None else []
    
    def copy(self) -> 'State':
        return State(self.current_port, self.capital, self.time,
                    self.used_capacity, self.route.copy(), 
                    self.inventory.copy())

# Solución principal usando Simulated Annealing
def solve(
    n: int,
    d: List[List[float]],                 # d[i][j] = d_{ij}
    t_max: float,                         # T_max
    c_max: float,                         # C_max
    k_0: float,                           # K_0
    k_min: float,                         # K_min
    items_by_port: List[List[Item]]       # M_i para cada puerto i
) -> float:
    """
    Resuelve el problema del Comerciante Holandés usando Simulated Annealing.
    Retorna el máximo capital final alcanzable.
    """
    
    def greedy_initial_solution() -> State:
        """Genera una solución inicial usando heurística greedy."""
        state = State(current_port=0, capital=k_0, time=0.0, 
                     used_capacity=0.0, route=[0], inventory=[])
        
        unvisited = set(range(1, n))  # Todos los puertos excepto Amsterdam
        
        while unvisited:
            # Vender mercancías en el puerto actual si es beneficioso
            state = sell_in_current_port(state, items_by_port)

            # Elegir próximo puerto
            next_port = select_next_port_greedy(state, unvisited, d, t_max)
            
            if next_port is None:
                break
            
            # Viajar al siguiente puerto
            travel_time = d[state.current_port][next_port]
            if state.time + travel_time > t_max:
                break
            
            # Comprar mercancías prometedoras
            state = buy_in_current_port(state, items_by_port, next_port)
                                        
            state.time += travel_time
            state.current_port = next_port
            state.route.append(next_port)
            unvisited.remove(next_port)
        
        # Regresar a Amsterdam si es posible
        travel_back = d[state.current_port][0]
        if state.time + travel_back <= t_max:
            state.time += travel_back
            state.current_port = 0
            state.route.append(0)
        
        # Vender todo en Amsterdam
        state = sell_all_in_amsterdam(state, items_by_port)
        
        return state
    
    def sell_in_current_port(state: State, items_by_port: List[List[Item]]) -> State:
        """Vende mercancías en el puerto actual si es beneficioso."""
        new_state = state.copy()
        new_inventory = []
        
        for merch in state.inventory:
            i, k, w, buy_price = merch
            # Solo vender si el precio de venta actual es mayor que el de compra
            # y no estamos en el puerto donde se compró
            if i != state.current_port:
                sell_price = items_by_port[state.current_port][k].sell_price
                if sell_price > buy_price:
                    new_state.capital += sell_price
                    # No agregar al inventario (se vendió)
                else:
                    new_inventory.append(merch)
            else:
                new_inventory.append(merch)
        
        new_state.inventory = new_inventory
        return new_state
    
    def buy_in_current_port(state: State, items_by_port: List[List[Item]], next_port: int) -> State:
        """Compra mercancías usando mochila 0/1 para optimizar."""
        new_state = state.copy()
        port = state.current_port
        
        # Capacidad y capital disponibles
        available_capacity = c_max - state.used_capacity
        available_capital = state.capital - k_min
        
        # Filtrar items que podemos comprar
        candidate_items = []
        for k, item in enumerate(items_by_port[state.current_port]):
            if item.w <= available_capacity and item.buy_price <= available_capital:
                # Estimar ganancia (simple heurística)
                estimated_profit = items_by_port[next_port][k].sell_price - item.buy_price
                if estimated_profit > 0:
                    candidate_items.append((k, item.w, item.buy_price, estimated_profit))
        
        if not candidate_items:
            return new_state
        
        # Mochila 0/1 simplificada (para capacidad)
        # Ordenar por profit/weight ratio
        candidate_items.sort(key=lambda x: x[3]/x[1], reverse=True)
        
        for k, weight, buy_price, profit in candidate_items:
            if (available_capacity >= weight and 
                available_capital >= buy_price):
                # Comprar el item
                new_state.capital -= buy_price
                new_state.used_capacity += weight
                new_state.inventory.append(
                    Merchandise(port, k, weight, buy_price)
                )
                available_capacity -= weight
                available_capital -= buy_price
        
        new_state.capital -= k_min
        return new_state
    
    def select_next_port_greedy(state: State, unvisited: Set[int], 
                               d: List[List[float]], t_max: float) -> Optional[int]:
        """Selecciona el próximo puerto usando heurística greedy."""
        best_port = None
        best_score = -float('inf')
        current = state.current_port
        
        for port in unvisited:
            travel_time = d[current][port]
            time_back = d[port][0] if port != 0 else 0
            total_time = state.time + travel_time + time_back
            
            if total_time <= t_max:
                # Score heurístico: cuanto más cerca y más items tenga
                # Podemos mejorarlo considerando el potencial de ganancia
                distance_score = 1.0 / (travel_time + 1e-6)
                items_count = len(items_by_port[port])
                item_score = min(items_count / 10.0, 1.0)  # Normalizado
                
                score = distance_score + item_score
                
                if score > best_score:
                    best_score = score
                    best_port = port
        
        return best_port
    
    def sell_all_in_amsterdam(state: State, items_by_port: List[List[Item]]) -> State:
        """Vende todo el inventario en Amsterdam."""
        new_state = state.copy()
        
        for merch in state.inventory:
            i, k, w, buy_price = merch
            # Vender en Amsterdam (puerto 0)
            sell_price = items_by_port[0][k].sell_price
            new_state.capital += sell_price
        
        new_state.inventory = []
        return new_state
    
    def evaluate_state(state: State, items_by_port: List[List[Item]]) -> float:
        """Evalúa un estado (capital final después de vender en Amsterdam)."""
        # Primero simular venta de todo en Amsterdam
        total_capital = state.capital
        
        for merch in state.inventory:
            i, k, w, buy_price = merch
            sell_price = items_by_port[0][k].sell_price if k < len(items_by_port[0]) else 0
            total_capital += sell_price
        
        return total_capital
    
    def simulate_route(route: List[int], d: List[List[float]], 
                      items_by_port: List[List[Item]]) -> Optional[State]:
        """Simula una ruta completa y retorna el estado final."""
        if not route or route[0] != 0:
            return None
        
        state = State(current_port=0, capital=k_0, time=0.0,
                     used_capacity=0.0, route=[0], inventory=[])
        
        for i in range(1, len(route)):
            next_port = route[i]
            travel_time = d[state.current_port][next_port]
            
            # Verificar tiempo
            if state.time + travel_time > t_max:
                return None
            
            # Viajar
            state.time += travel_time
            state.current_port = next_port
            
            # Vender
            state = sell_in_current_port(state, items_by_port)
            
            # Comprar
            state = buy_in_current_port(state, items_by_port, next_port)
            
            # Verificar restricciones
            if state.capital < 0 or state.used_capacity > c_max:
                return None
            
            # Actualizar ruta
            state.route.append(next_port)
        
        # Regresar a Amsterdam si no estamos ya allí
        if state.current_port != 0:
            travel_back = d[state.current_port][0]
            if state.time + travel_back > t_max:
                return None
            state.time += travel_back
            state.current_port = 0
            state.route.append(0)
        
        # Vender todo en Amsterdam
        state = sell_all_in_amsterdam(state, items_by_port)
        
        return state
    
    def generate_neighbor(state: State) -> List[int]:
        """Genera una ruta vecina modificando la ruta actual."""
        route = state.route.copy()
        
        if len(route) <= 3:  # Solo Amsterdam + 1 puerto + Amsterdam
            # Insertar un puerto aleatorio
            available = [p for p in range(1, n) if p not in route]
            if available:
                insert_pos = random.randint(1, len(route)-1)
                insert_port = random.choice(available)
                route.insert(insert_pos, insert_port)
            return route
        
        operation = random.choice(['swap', 'insert', 'remove', 'reverse'])
        
        if operation == 'swap':
            # Intercambiar dos puertos (no Amsterdam)
            i = random.randint(1, len(route)-2)
            j = random.randint(1, len(route)-2)
            if i != j:
                route[i], route[j] = route[j], route[i]
        
        elif operation == 'insert':
            # Insertar un puerto no visitado
            visited = set(route)
            available = [p for p in range(1, n) if p not in visited]
            if available:
                insert_pos = random.randint(1, len(route)-1)
                insert_port = random.choice(available)
                route.insert(insert_pos, insert_port)
        
        elif operation == 'remove':
            # Remover un puerto (no Amsterdam)
            if len(route) > 3:
                remove_pos = random.randint(1, len(route)-2)
                route.pop(remove_pos)
        
        elif operation == 'reverse':
            # Invertir un segmento
            i = random.randint(1, len(route)-2)
            j = random.randint(i, len(route)-2)
            route[i:j+1] = reversed(route[i:j+1])
        
        # Asegurar que empieza y termina en Amsterdam
        if route[0] != 0:
            route.insert(0, 0)
        if route[-1] != 0:
            route.append(0)
        
        # Eliminar Amsterdams consecutivos
        cleaned_route = [route[0]]
        for i in range(1, len(route)):
            if not (route[i] == 0 and route[i-1] == 0):
                cleaned_route.append(route[i])
        
        return cleaned_route
    
    def simulated_annealing(initial_state: State, max_iter: int = 3000) -> State:
        """Algoritmo de Simulated Annealing para mejorar la solución."""
        current_state = initial_state
        best_state = initial_state.copy()
        current_value = evaluate_state(current_state, items_by_port)
        best_value = current_value
        
        temperature = 1000.0
        cooling_rate = 0.995
        
        for iteration in range(max_iter):
            # Generar vecino
            new_route = generate_neighbor(current_state)
            new_state = simulate_route(new_route, d, items_by_port)
            
            if new_state is None:
                continue
            
            new_value = evaluate_state(new_state, items_by_port)
            
            # Criterio de aceptación
            delta = new_value - current_value
            
            if delta > 0 or random.random() < math.exp(delta / temperature):
                current_state = new_state
                current_value = new_value
                
                if current_value > best_value:
                    best_state = current_state.copy()
                    best_value = current_value
            
            # Enfriar
            temperature *= cooling_rate
            
            # Reinicio ocasional
            if iteration % 500 == 0 and temperature < 10:
                temperature = 100.0
        
        return best_state
    
    initial_state = greedy_initial_solution()
    best_state = simulated_annealing(initial_state, max_iter=2000)
    final_capital = evaluate_state(best_state, items_by_port)
    
    return final_capital