import sys
import importlib.util
from pathlib import Path

def setup_imports():
    """Configura las rutas de importación."""
    # Obtener el directorio actual (tester)
    current_dir = Path(__file__).parent
    # Directorio src (padre de tester)
    src_dir = current_dir.parent
    # Directorio solutions
    solutions_dir = src_dir / "solutions"
    
    # Añadir a sys.path
    sys.path.insert(0, str(src_dir))
    sys.path.insert(0, str(solutions_dir))
    
    return src_dir, solutions_dir

def import_module_from_file(file_path):
    """Importa un módulo desde un archivo."""
    module_name = file_path.stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def load_algorithms():
    """Carga los algoritmos desde solutions."""
    algorithms = {}
    
    # Configurar imports
    src_dir, solutions_dir = setup_imports()
    
    # Intentar cargar JAT
    jat_file = solutions_dir / "brute_force_JAT.py"
    if jat_file.exists():
        try:
            # Importar directamente el módulo
            spec = importlib.util.spec_from_file_location("brute_force_JAT", jat_file)
            jat_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(jat_module)
            algorithms['JAT'] = jat_module.solve
            print("✓ Algoritmo JAT cargado")
        except Exception as e:
            print(f"✗ Error cargando JAT: {e}")
            algorithms['JAT'] = None
    else:
        print("✗ Archivo brute_force_JAT.py no encontrado")
        algorithms['JAT'] = None
    
    # Intentar cargar CHP
    chp_file = solutions_dir / "brute_force_CHP.py"
    if chp_file.exists():
        try:
            spec = importlib.util.spec_from_file_location("brute_force_CHP", chp_file)
            chp_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chp_module)
            algorithms['CHP'] = chp_module.solve
            print("✓ Algoritmo CHP cargado")
        except Exception as e:
            print(f"✗ Error cargando CHP: {e}")
            algorithms['CHP'] = None
    else:
        print("✗ Archivo brute_force_CHP.py no encontrado")
        algorithms['CHP'] = None
    
    return algorithms

def run_test_case(case_num, algorithms, test_cases_dir="test_cases"):
    """Ejecuta un caso de prueba individual."""
    print(f"\n{'='*60}")
    print(f"CASO DE PRUEBA {case_num}")
    print(f"{'='*60}")
    
    # Construir rutas
    current_dir = Path(__file__).parent
    test_case_file = current_dir / test_cases_dir / f"test_case_{case_num}.py"
    
    if not test_case_file.exists():
        print(f"Error: No se encuentra el archivo {test_case_file}")
        return None, None, "NO_FILE"
    
    try:
        # Importar el caso de prueba
        test_case = import_module_from_file(test_case_file)
        
        # Obtener datos del caso
        n = test_case.n
        d = test_case.d
        t_max = test_case.t_max
        c_max = test_case.c_max
        k_0 = test_case.k_0
        k_min = test_case.k_min
        items_by_port = test_case.items_by_port
        
        print(f"Parámetros:")
        print(f"  n={n}, t_max={t_max:.1f}, c_max={c_max:.1f}")
        print(f"  k_0={k_0:.1f}, k_min={k_min:.1f}")
        print(f"  Puertos: {n}, Ítems por puerto: {[len(items) for items in items_by_port]}")
        
        results = {}
        
        # Ejecutar cada algoritmo disponible
        for algo_name, algo_func in algorithms.items():
            if algo_func is not None:
                print(f"\nEjecutando algoritmo {algo_name}...")
                try:
                    result = algo_func(n, d, t_max, c_max, k_0, k_min, items_by_port)
                    results[algo_name] = result
                    print(f"  Resultado {algo_name}: {result}")
                except Exception as e:
                    print(f"  Error en {algo_name}: {e}")
                    import traceback
                    traceback.print_exc()
                    results[algo_name] = None
        
        # Comparar resultados
        if len(results) == 0:
            print("\n✗ No hay algoritmos disponibles para ejecutar")
            return None, None, "NO_ALGORITHMS"
        
        elif len(results) == 1:
            algo_name = list(results.keys())[0]
            result = results[algo_name]
            print(f"\nℹ️  Solo disponible {algo_name}: {result}")
            return {algo_name: result}, f"Solo {algo_name}", "SINGLE"
        
        else:
            # Tenemos ambos algoritmos
            result_JAT = results.get('JAT')
            result_CHP = results.get('CHP')
            
            if result_JAT is None or result_CHP is None:
                available = []
                if result_JAT is not None:
                    available.append(f"JAT={result_JAT}")
                if result_CHP is not None:
                    available.append(f"CHP={result_CHP}")
                print(f"\nℹ️  Resultados parciales: {', '.join(available)}")
                return results, "Parciales", "PARTIAL"
            
            # Comparar valores
            if result_JAT == -1 and result_CHP == -1:
                print(f"\n✓ Ambos algoritmos retornan -1 (sin solución)")
                return results, "Ambos -1", "MATCH"
            elif abs(result_JAT - result_CHP) < 0.01:
                print(f"\n✓ Los resultados coinciden: {result_JAT:.2f}")
                return results, f"Coinciden: {result_JAT:.2f}", "MATCH"
            else:
                print(f"\n✗ Los resultados difieren:")
                print(f"  JAT: {result_JAT}")
                print(f"  CHP: {result_CHP}")
                print(f"  Diferencia: {abs(result_JAT - result_CHP):.2f}")
                return results, f"Difieren: JAT={result_JAT}, CHP={result_CHP}", "DIFFERENT"
            
    except Exception as e:
        print(f"\n✗ Error al procesar caso {case_num}: {e}")
        import traceback
        traceback.print_exc()
        return None, str(e), "ERROR"

def validate_all_cases(num_cases=5, test_cases_dir="test_cases"):
    """Valida todos los casos de prueba."""
    print("="*70)
    print("VALIDACIÓN DE ALGORITMOS - COMPAÑÍA HOLANDESA")
    print("="*70)
    
    # Cargar algoritmos una sola vez
    print("\nCargando algoritmos...")
    algorithms = load_algorithms()
    
    if not any(algorithms.values()):
        print("\n✗ No se pudo cargar ningún algoritmo. Verifica:")
        print("  1. Que los archivos existen en solutions/")
        print("  2. Que tienen la función solve() definida")
        print("  3. Que no hay errores de sintaxis en los algoritmos")
        return
    
    available_algs = [name for name, func in algorithms.items() if func is not None]
    print(f"\nAlgoritmos disponibles: {', '.join(available_algs)}")
    
    results = []
    
    # Ejecutar cada caso
    for case_num in range(1, num_cases + 1):
        case_results, message, status = run_test_case(case_num, algorithms, test_cases_dir)
        results.append((case_num, case_results, message, status))
    
    # Generar resumen
    print("\n" + "="*70)
    print("RESUMEN DE VALIDACIÓN")
    print("="*70)
    
    summary = {
        "MATCH": 0,
        "DIFFERENT": 0,
        "SINGLE": 0,
        "PARTIAL": 0,
        "ERROR": 0,
        "NO_FILE": 0,
        "NO_ALGORITHMS": 0
    }
    
    for case_num, case_results, message, status in results:
        summary[status] = summary.get(status, 0) + 1
        
        # Mostrar estado
        if status == "MATCH":
            symbol = "✓"
        elif status == "DIFFERENT":
            symbol = "✗"
        elif status == "ERROR":
            symbol = "!"
        else:
            symbol = "ℹ️"
        
        print(f"Caso {case_num:2d}: {symbol} {status:15} - {message}")
    
    # Estadísticas finales
    print(f"\n{'='*70}")
    print("ESTADÍSTICAS FINALES")
    print(f"{'='*70}")
    print(f"Total casos: {num_cases}")
    print(f"Coincidencias: {summary['MATCH']}")
    print(f"Diferencias: {summary['DIFFERENT']}")
    print(f"Solo un algoritmo: {summary['SINGLE']}")
    print(f"Parciales: {summary['PARTIAL']}")
    print(f"Errores: {summary['ERROR'] + summary['NO_FILE'] + summary['NO_ALGORITHMS']}")
    
    if summary['DIFFERENT'] > 0:
        print(f"\n⚠️  ATENCIÓN: Se encontraron {summary['DIFFERENT']} casos con resultados diferentes.")
        print("   Revisa los algoritmos para encontrar la discrepancia.")
    
    if summary['MATCH'] == num_cases:
        print(f"\n🎉 ¡TODOS LOS CASOS COINCIDEN! Los algoritmos son consistentes.")
    
    return results

if __name__ == "__main__":
    # Crear la ruta a test_cases
    num_cases = 0
    if len(sys.argv) < 2:
        print("ERROR: Debes especificar el número total de casos a validar.")
        print("Uso: python -m tester.validator <num_cases>")
        print("Ejemplo: python -m tester.validator 100")
        sys.exit(1)
    
    try:
        num_cases = int(sys.argv[1])
        if num_cases <= 0:
            print(f"ERROR: El número total debe ser mayor que 0, recibido: {num_cases}")
            sys.exit(1)
    except ValueError:
        print(f"ERROR: El argumento debe ser un número entero, recibido: {sys.argv[1]}")
        sys.exit(1)
         
    test_dir = Path(__file__).parent / "test_cases"
    
    if num_cases == 0:
        print("No se encontraron casos de prueba en test_cases/")
        print("Ejecuta primero: python -m tester.generator")
    else:
        print(f"Encontrados {num_cases} casos de prueba.")
        validate_all_cases(num_cases, "test_cases")