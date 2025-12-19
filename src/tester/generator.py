import random
import math
from typing import List, Tuple
from pathlib import Path

# Añadir el directorio padre al path para importar utils
import sys
src_dir = Path(__file__).parent.parent
sys.path.insert(0, str(src_dir))
sys.path.insert(0, str(src_dir / "solutions"))

from solutions.utils import Item

def enforce_triangle_inequality(d: List[List[float]]) -> List[List[float]]:
    """Aplica el algoritmo de Floyd-Warshall para asegurar la desigualdad triangular."""
    n = len(d)
    # Hacer una copia
    dist = [row[:] for row in d]
    
    # Aplicar Floyd-Warshall para encontrar caminos más cortos
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j] + 1e-9:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    dist[j][i] = dist[i][j]
    
    return dist

def generate_random_instance(
    min_ports: int = 3,
    max_ports: int = 5,
    min_items: int = 2,  # Mínimo número de tipos de mercancías (m)
    max_items: int = 4,  # Máximo número de tipos de mercancías (m)
    seed: int = None
) -> Tuple[int, List[List[float]], float, float, float, float, List[List[Item]]]:
    """
    Genera una instancia aleatoria del problema de la Compañía Holandesa.
    TODOS los puertos tienen exactamente m tipos de mercancías.
    """
    if seed is not None:
        random.seed(seed)
    
    # 1. Generar número de puertos
    n = random.randint(min_ports, max_ports)
    
    # 2. Generar número de tipos de mercancías (m) - IGUAL PARA TODOS LOS PUERTOS
    m = random.randint(min_items, max_items)
    
    # 3. Generar matriz de distancias (simétrica, con 0 en diagonal) y con desigualdad triangular
    coordinates = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]
    
    d = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[j]
            distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            d[i][j] = round(distance, 1)
            d[j][i] = round(distance, 1)
            
    d = enforce_triangle_inequality(d)
    # for i in range(n):
    #     for j in range(n):
    #         d[i][j] = round(d[i][j], 1)
    
    # 4. Generar tiempo máximo
    if n > 1:
        min_distance_to_other = min([d[0][i] for i in range(1, n)])
        second_min = sorted([d[0][i] for i in range(1, n)])[1] if n > 2 else min_distance_to_other
        
        t_max = random.uniform(
            min_distance_to_other * 2 + 0.5,
            min_distance_to_other * 4 + second_min * 2
        )
        t_max = round(t_max, 1)
    else:
        t_max = 10.0
    
    # 5. Generar capacidad máxima de carga
    c_max = random.uniform(5, 20)
    c_max = round(c_max, 1)
    
    # 6. Generar capital inicial
    k_0 = random.uniform(10, 50)
    k_0 = round(k_0, 1)
    
    # 7. Generar capital mínimo
    k_min_percent = random.uniform(0.1, 0.3)
    k_min = round(k_0 * k_min_percent, 1)
    
    # 8. Generar ítems por puerto - TODOS LOS PUERTOS TIENEN EXACTAMENTE m TIPOS
    items_by_port = []
    
    # Primero, generar los m tipos para Ámsterdam (puerto 0)
    # En Ámsterdam, todos los ítems tienen w=inf, buy=inf, sell=-inf
    amsterdam_items = []
    for _ in range(m):
        amsterdam_items.append(Item(
            w=float('inf'),
            buy_price=float('inf'),
            sell_price=float('-inf')
        ))
    items_by_port.append(amsterdam_items)
    
    # Luego, generar para los otros puertos (1 a n-1)
    for port in range(1, n):
        port_items = []
        
        for item_index in range(m):  # Exactamente m tipos por puerto
            # Peso aleatorio (entre 1 y c_max/2 para que sea posible cargar varios)
            w = random.uniform(1, c_max / 2)
            w = round(w, 1)
            
            # Precio de compra (asegurar que k_0 puede comprar al menos un ítem)
            max_buy_price = k_0 * 1.5
            buy_price = random.uniform(1, max_buy_price)
            buy_price = round(buy_price, 1)
            
            # Precio de venta
            # Algunos ítems pueden no ser rentables (venta < compra)
            profit_margin = random.uniform(0.8, 1.5)  # 0.8 = pérdida, 1.5 = ganancia
            sell_price = round(buy_price * profit_margin, 1)
            
            # Asegurar que al menos algunos ítems sean rentables
            if random.random() < 0.7:  # 70% de ítems rentables
                sell_price = max(sell_price, buy_price * 1.1)  # Al menos 10% de ganancia
            
            # Redondear para evitar problemas de precisión flotante
            sell_price = round(sell_price, 2)
            
            port_items.append(Item(w=w, buy_price=buy_price, sell_price=sell_price))
        
        items_by_port.append(port_items)
    
    # 9. Asegurar que haya al menos una solución factible
    if n > 1:
        feasible = False
        for i in range(1, n):
            if d[0][i] * 2 <= t_max:
                feasible = True
                break
        
        if not feasible:
            min_round_trip = min([d[0][i] * 2 for i in range(1, n)])
            t_max = min_round_trip + random.uniform(0.5, 2.0)
            t_max = round(t_max, 1)
    
    return n, d, t_max, c_max, k_0, k_min, items_by_port

def print_instance(
    n: int,
    d: List[List[float]],
    t_max: float,
    c_max: float,
    k_0: float,
    k_min: float,
    items_by_port: List[List[Item]]
):
    """Imprime una instancia del problema en formato legible."""
    m = len(items_by_port[0]) if items_by_port else 0
    
    print(f"n = {n}")
    print(f"m = {m} (tipos de mercancías por puerto)")
    print("\nMatriz de distancias (d):")
    for row in d:
        print("  " + " ".join([f"{x:5.1f}" for x in row]))
    
    print(f"\nt_max = {t_max:.1f}")
    print(f"c_max = {c_max:.1f}")
    print(f"k_0 = {k_0:.1f}")
    print(f"k_min = {k_min:.1f}")
    
    print(f"\nÍtems por puerto (todos tienen exactamente {m} tipos):")
    for i, items in enumerate(items_by_port):
        print(f"  Puerto {i} ({len(items)} tipos):")
        for j, item in enumerate(items):
            if item.w == float('inf'):
                print(f"    Ítem {j}: w=inf, buy=inf, sell=-inf")
            else:
                print(f"    Ítem {j}: w={item.w:.1f}, buy={item.buy_price:.1f}, sell={item.sell_price:.1f}")

def save_instance_to_file(
    filename: str,
    n: int,
    d: List[List[float]],
    t_max: float,
    c_max: float,
    k_0: float,
    k_min: float,
    items_by_port: List[List[Item]]
):
    """Guarda una instancia en un archivo Python ejecutable."""
    m = len(items_by_port[0]) if items_by_port else 0
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("from math import inf\n")
        f.write("from typing import List\n")
        f.write("from solutions.utils import Item\n\n")
        
        f.write(f"n = {n}\n")
        f.write(f"# m = {m} tipos de mercancías por puerto\n\n")
        
        f.write("d: List[List[float]] = [\n")
        for row in d:
            f.write(f"    {row},\n")
        f.write("]\n\n")
        
        f.write(f"t_max: float = {t_max}\n")
        f.write(f"c_max: float = {c_max}\n")
        f.write(f"k_0: float = {k_0}\n")
        f.write(f"k_min: float = {k_min}\n\n")
        
        f.write(f"# Lista de {n} listas, cada una con {m} ítems\n")
        f.write("items_by_port: List[List[Item]] = [\n")
        for port_items in items_by_port:
            items_str = "[" + ", ".join([
                f"Item({item.w}, {item.buy_price}, {item.sell_price})" 
                for item in port_items
            ]) + "]"
            f.write(f"    {items_str},\n")
        f.write("]\n")

def generate_solution_file(filename: str, n: int, d: List[List[float]], 
                          t_max: float, c_max: float, k_0: float, 
                          k_min: float, items_by_port: List[List[Item]], 
                          case_num: int):
    """Genera un archivo que ejecuta ambos algoritmos y compara resultados."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# Solución para caso de prueba {case_num}\n")
        f.write("from math import inf\n")
        f.write("from typing import List\n")
        f.write("import sys\n")
        f.write("import os\n")
        f.write("from pathlib import Path\n\n")
        
        f.write("# Configurar rutas de importación\n")
        f.write("current_dir = Path(__file__).parent\n")
        f.write("src_dir = current_dir.parent\n")
        f.write("solutions_dir = src_dir / 'solutions'\n")
        f.write("sys.path.insert(0, str(src_dir))\n")
        f.write("sys.path.insert(0, str(solutions_dir))\n\n")
        
        f.write("from solutions.utils import Item\n\n")
        
        f.write("# Intentar importar algoritmos\n")
        f.write("try:\n")
        f.write("    from solutions.brute_force_JAT import solve as solve_JAT\n")
        f.write("    JAT_available = True\n")
        f.write("except ImportError as e:\n")
        f.write("    print(f'Algoritmo JAT no disponible: {e}')\n")
        f.write("    solve_JAT = None\n")
        f.write("    JAT_available = False\n\n")
        
        f.write("try:\n")
        f.write("    from solutions.brute_force_CHP import solve as solve_CHP\n")
        f.write("    CHP_available = True\n")
        f.write("except ImportError as e:\n")
        f.write("    print(f'Algoritmo CHP no disponible: {e}')\n")
        f.write("    solve_CHP = None\n")
        f.write("    CHP_available = False\n\n")
        
        # Datos de la instancia
        f.write(f"# Datos del caso {case_num}\n")
        f.write(f"n = {n}\n\n")
        
        f.write("d = [\n")
        for row in d:
            f.write(f"    {row},\n")
        f.write("]\n\n")
        
        f.write(f"t_max = {t_max}\n")
        f.write(f"c_max = {c_max}\n")
        f.write(f"k_0 = {k_0}\n")
        f.write(f"k_min = {k_min}\n\n")
        
        f.write("items_by_port = [\n")
        for port_items in items_by_port:
            items_str = "[" + ", ".join([
                f"Item({item.w}, {item.buy_price}, {item.sell_price})" 
                for item in port_items
            ]) + "]"
            f.write(f"    {items_str},\n")
        f.write("]\n\n")
        
        # Ejecución de algoritmos
        f.write("# Ejecutar algoritmos\n")
        f.write(f"print('=== Caso de prueba {case_num} ===')\n")
        f.write(f"print(f\"n={{n}}, t_max={{t_max}}, c_max={{c_max}}, k_0={{k_0}}, k_min={{k_min}}\")\n\n")
        
        f.write("# Ejecutar JAT si está disponible\n")
        f.write("if JAT_available:\n")
        f.write("    print('\\\\nEjecutando algoritmo JAT...')\n")
        f.write("    try:\n")
        f.write("        result_JAT = solve_JAT(n, d, t_max, c_max, k_0, k_min, items_by_port)\n")
        f.write("        print(f'Resultado JAT: {{result_JAT}}')\n")
        f.write("    except Exception as e:\n")
        f.write("        print(f'Error en JAT: {{e}}')\n")
        f.write("        import traceback\n")
        f.write("        traceback.print_exc()\n")
        f.write("        result_JAT = None\n")
        f.write("else:\n")
        f.write("    result_JAT = None\n\n")
        
        f.write("# Ejecutar CHP si está disponible\n")
        f.write("if CHP_available:\n")
        f.write("    print('\\\\nEjecutando algoritmo CHP...')\n")
        f.write("    try:\n")
        f.write("        result_CHP = solve_CHP(n, d, t_max, c_max, k_0, k_min, items_by_port)\n")
        f.write("        print(f'Resultado CHP: {{result_CHP}}')\n")
        f.write("    except Exception as e:\n")
        f.write("        print(f'Error en CHP: {{e}}')\n")
        f.write("        import traceback\n")
        f.write("        traceback.print_exc()\n")
        f.write("        result_CHP = None\n")
        f.write("else:\n")
        f.write("    result_CHP = None\n\n")
        
        # Comparación
        f.write("# Comparar resultados\n")
        f.write("if result_JAT is not None and result_CHP is not None:\n")
        f.write("    if result_JAT == -1 and result_CHP == -1:\n")
        f.write("        print(f'\\\\n[OK] Ambos algoritmos retornan -1 (sin solución)')\n")
        f.write("    elif abs(result_JAT - result_CHP) < 0.01:\n")
        f.write("        print(f'\\\\n[OK] Los resultados coinciden: {{result_JAT:.2f}}')\n")
        f.write("    else:\n")
        f.write("        print(f'\\\\n[ERROR] Los resultados difieren: JAT={{result_JAT:.2f}}, CHP={{result_CHP:.2f}}')\n")
        f.write("        print(f'         Diferencia: {{abs(result_JAT - result_CHP):.2f}}')\n")
        f.write("elif result_JAT is not None:\n")
        f.write("    print(f'\\\\n[Solo JAT] Resultado: {{result_JAT:.2f}}')\n")
        f.write("elif result_CHP is not None:\n")
        f.write("    print(f'\\\\n[Solo CHP] Resultado: {{result_CHP:.2f}}')\n")
        f.write("else:\n")
        f.write("    print('\\\\n[Error] Ningún algoritmo disponible o todos fallaron')\n")

def create_init_file(directory: Path):
    """Crea un archivo __init__.py en el directorio especificado."""
    init_file = directory / "__init__.py"
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write("# Paquete de casos de prueba para la Compañía Holandesa\n")
        f.write("# Generado automáticamente\n\n")
        f.write("__version__ = '1.0.0'\n")
        f.write("__author__ = 'Generador de Casos'\n")

def generate_test_cases(num_cases: int = 5, output_dir: str = "test_cases"):
    """Genera múltiples casos de prueba y los guarda en archivos."""
    # Crear directorio si no existe
    output_path = Path(__file__).parent / output_dir
    output_path.mkdir(exist_ok=True)
    
    # Crear archivo __init__.py en la carpeta test_cases
    create_init_file(output_path)
    
    print(f"\nGenerando {num_cases} casos de prueba...")
    
    for i in range(num_cases):
        print(f"  Caso {i+1}/{num_cases}...")
        
        # Generar instancia con m constante para todos los puertos
        instance = generate_random_instance(
            min_ports=3,
            max_ports=5,
            min_items=2,  # Mínimo 2 tipos de mercancías
            max_items=4,  # Máximo 4 tipos de mercancías
            seed=i
        )
        
        # Guardar instancia básica
        case_file = output_path / f"test_case_{i+1}.py"
        save_instance_to_file(str(case_file), *instance)
        
        # Generar archivo de solución
        solution_file = output_path / f"test_case_{i+1}_solution.py"
        generate_solution_file(str(solution_file), *instance, case_num=i+1)
    
    print(f"\n✓ Generados {num_cases} casos de prueba en '{output_dir}/'")
    print(f"  Cada puerto tiene exactamente m tipos de mercancías (m constante)")
    
# Función principal para ejecutar desde la línea de comandos
def main():
    """Función principal del generador."""
    print("="*70)
    print("GENERADOR DE CASOS DE PRUEBA - COMPAÑÍA HOLANDESA")
    print("="*70)
    
    # Generar múltiples casos de prueba
    print("\n1. Generando casos de prueba para validación...")
    generate_test_cases(num_cases=100, output_dir="test_cases")
    
    print("\n" + "="*70)
    print("INSTRUCCIONES DE USO:")
    print("="*70)    
    print("\nPara validar todos los casos:")
    print("  python -m tester.validator")

if __name__ == "__main__":
    main()