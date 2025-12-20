#!/usr/bin/env python3
"""
Validator para ejecutar casos de prueba y verificar si los resultados coinciden.
Ejecuta los archivos test_case_*_solution.py de tester/test_cases/
"""

import subprocess
import sys
import re
from pathlib import Path

def parse_results(output: str):
    """Extrae los resultados brute y efficient de la salida."""
    brute_result = None
    efficient_result = None
    status = "unknown"
    
    # Buscar resultados brute (JAT)
    brute_match = re.search(r'Resultado JAT:\s*(-?\d*\.?\d+)', output)
    if brute_match:
        brute_result = float(brute_match.group(1))
    
    # Buscar resultados efficient (CHP)  
    efficient_match = re.search(r'Resultado CHP:\s*(-?\d*\.?\d+)', output)
    if efficient_match:
        efficient_result = float(efficient_match.group(1))
    
    # Determinar estado
    if "[OK] Los resultados coinciden" in output:
        status = "OK"
    elif "[OK] Ambos algoritmos retornan -1" in output:
        status = "OK"
    elif "[ERROR] Los resultados difieren" in output:
        status = "ERROR"
    elif "[Solo JAT]" in output:
        status = "SOLO_BRUTE"
    elif "[Solo CHP]" in output:
        status = "SOLO_EFFICIENT"
    elif "[Error] Ningún algoritmo" in output:
        status = "FAILED"
    
    return brute_result, efficient_result, status

def main():
    print("🚀 Validator - Comparador de Algoritmos")
    print("=" * 50)
    
    # Directorio actual del validador (tester/)
    current_dir = Path(__file__).parent
    test_cases_dir = current_dir / "test_cases"
    
    if not test_cases_dir.exists():
        print(f"❌ No se encuentra la carpeta: {test_cases_dir}")
        return 1
    
    # Buscar archivos test_case_*_solution.py
    test_files = []
    for file in test_cases_dir.glob("test_case_*_solution.py"):
        test_files.append(file)
    
    # Ordenar por número
    def get_case_number(filename):
        name = filename.stem
        parts = name.split('_')
        return int(parts[2])
    
    test_files.sort(key=get_case_number)
    
    if not test_files:
        print("❌ No se encontraron archivos test_case_*_solution.py")
        return 1
    
    print(f"📁 Encontrados {len(test_files)} casos de prueba\n")
    
    results = []
    
    for test_file in test_files:
        case_num = get_case_number(test_file)
        print(f"{'='*60}")
        print(f"📊 Caso {case_num}: {test_file.name}")
        print(f"{'='*60}")
        
        try:
            # Ejecutar el archivo
            result = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parsear resultados
            brute_result, efficient_result, status = parse_results(result.stdout)
            
            # Determinar si coinciden
            passed = False
            details = ""
            
            if status == "OK":
                passed = True
                if brute_result == -1 and efficient_result == -1:
                    details = "Ambos: -1 (sin solución)"
                else:
                    details = f"✓ Coinciden: {brute_result:.2f}"
            elif status == "ERROR":
                passed = False
                difference = abs(brute_result - efficient_result) if brute_result is not None and efficient_result is not None else None
                if difference is not None:
                    details = f"✗ Difieren: brute={brute_result:.2f}, efficient={efficient_result:.2f} (diff={difference:.2f})"
                else:
                    details = "✗ Resultados diferentes"
            elif status == "SOLO_BRUTE":
                passed = True  # Asumimos OK si solo uno está disponible
                details = f"⚠️ Solo brute: {brute_result:.2f}"
            elif status == "SOLO_EFFICIENT":
                passed = True  # Asumimos OK si solo uno está disponible
                details = f"⚠️ Solo efficient: {efficient_result:.2f}"
            elif status == "FAILED":
                passed = False
                details = "💥 Ningún algoritmo disponible"
            else:
                # Verificar manualmente si los números coinciden
                if brute_result is not None and efficient_result is not None:
                    if abs(brute_result - efficient_result) < 0.01:
                        passed = True
                        status = "OK"
                        details = f"✓ Coinciden: {brute_result:.2f}"
                    else:
                        passed = False
                        status = "ERROR"
                        difference = abs(brute_result - efficient_result)
                        details = f"✗ Difieren: brute={brute_result:.2f}, efficient={efficient_result:.2f} (diff={difference:.2f})"
                else:
                    passed = False
                    details = "❌ No se pudieron extraer resultados"
            
            # Mostrar salida
            print(result.stdout)
            if result.stderr:
                print("⚠️  Errores:")
                print(result.stderr[:500])
            
            print(f"📋 {details}")
            
            results.append({
                'file': test_file.name,
                'case_num': case_num,
                'passed': passed,
                'status': status,
                'brute': brute_result,
                'efficient': efficient_result,
                'details': details,
                'stdout': result.stdout,
                'stderr': result.stderr
            })
            
        except subprocess.TimeoutExpired:
            print(f"⏰ TIMEOUT: Excedió 30 segundos")
            results.append({
                'file': test_file.name,
                'case_num': case_num,
                'passed': False,
                'status': 'TIMEOUT',
                'brute': None,
                'efficient': None,
                'details': 'Timeout expired',
                'stdout': '',
                'stderr': 'Timeout'
            })
        except Exception as e:
            print(f"💥 ERROR: {e}")
            results.append({
                'file': test_file.name,
                'case_num': case_num,
                'passed': False,
                'status': 'EXECUTION_ERROR',
                'brute': None,
                'efficient': None,
                'details': str(e),
                'stdout': '',
                'stderr': str(e)
            })
    
    # Resumen detallado
    print(f"\n{'='*80}")
    print("📊 RESUMEN DETALLADO")
    print(f"{'='*80}")
    
    passed_count = 0
    error_count = 0
    solo_count = 0
    failed_count = 0
    
    for result in results:
        if result['passed']:
            passed_count += 1
            symbol = "✓"
        else:
            if result['status'] == 'ERROR':
                error_count += 1
            elif result['status'] in ['SOLO_BRUTE', 'SOLO_EFFICIENT']:
                solo_count += 1
            else:
                failed_count += 1
            symbol = "✗"
        
        # Mostrar cada caso
        brute_str = f"{result['brute']:.2f}" if result['brute'] is not None else "N/A"
        efficient_str = f"{result['efficient']:.2f}" if result['efficient'] is not None else "N/A"
        
        print(f"{symbol} Caso {result['case_num']:3d}: brute={brute_str:8s} efficient={efficient_str:8s} | {result['details']}")
    
    # Resumen estadístico
    print(f"\n{'='*80}")
    print("📈 ESTADÍSTICAS")
    print(f"{'='*80}")
    
    total = len(results)
    print(f"Total casos: {total}")
    print(f"✓ Coinciden: {passed_count}")
    print(f"✗ Difieren:  {error_count}")
    print(f"⚠️  Solo uno: {solo_count}")
    print(f"💥 Fallidos: {failed_count}")
    
    if error_count > 0:
        print(f"\n🔍 CASOS CON DIFERENCIAS:")
        for result in results:
            if result['status'] == 'ERROR':
                difference = abs(result['brute'] - result['efficient']) if result['brute'] is not None and result['efficient'] is not None else None
                if difference is not None:
                    print(f"  • Caso {result['case_num']}: brute={result['brute']:.2f}, efficient={result['efficient']:.2f} (diff={difference:.4f})")
    
    # Guardar reporte detallado
    output_path = Path(__file__).parent / "results"
    output_path.mkdir(exist_ok=True)
    
    with open("tester/results/validation_report.txt", "w") as f:
        f.write("REPORTE DE VALIDACIÓN - Comparación brute vs efficient\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Total casos analizados: {total}\n")
        f.write(f"Casos con resultados coincidentes: {passed_count}\n")
        f.write(f"Casos con resultados diferentes: {error_count}\n")
        f.write(f"Casos con solo un algoritmo: {solo_count}\n")
        f.write(f"Casos fallidos: {failed_count}\n\n")
        
        f.write("DETALLE POR CASO:\n")
        f.write("-" * 60 + "\n\n")
        
        for result in results:
            f.write(f"Caso {result['case_num']}:\n")
            f.write(f"  Archivo: {result['file']}\n")
            f.write(f"  Estado: {'PASADO' if result['passed'] else 'FALLIDO'}\n")
            f.write(f"  Resultado brute: {result['brute'] if result['brute'] is not None else 'N/A'}\n")
            f.write(f"  Resultado efficient: {result['efficient'] if result['efficient'] is not None else 'N/A'}\n")
            # f.write(f"  Detalles: {result['details']}\n")
            
            if result['status'] == 'ERROR' and result['brute'] is not None and result['efficient'] is not None:
                difference = abs(result['brute'] - result['efficient'])
                f.write(f"  Diferencia: {difference:.6f}\n")
            
            if result['stderr']:
                f.write(f"  Errores: {result['stderr'][:300]}\n")
            
            f.write("\n")
    
    print(f"\n📄 Reporte detallado guardado en: validation_report.txt")
    
    # Mostrar recomendaciones basadas en resultados
    print(f"\n{'='*80}")
    print("💡 RECOMENDACIONES")
    print(f"{'='*80}")
    
    if error_count == 0 and failed_count == 0:
        print("✅ ¡Excelente! Todos los casos coinciden perfectamente.")
        print("   Ambos algoritmos (brute force y efficient) producen los mismos resultados.")
    elif error_count > 0:
        print("⚠️  Se encontraron diferencias entre brute force y efficient.")
        print("   Esto podría indicar:")
        print("   1. Bugs en uno de los algoritmos")
        print("   2. Diferentes interpretaciones del problema")
        print("   3. Errores de precisión numérica")
        print("\n   Revisa los casos con diferencias para debugging.")
    elif solo_count > 0:
        print("ℹ️  Algunos casos solo ejecutaron un algoritmo.")
        print("   Verifica que ambos algoritmos estén correctamente implementados.")
    
    # Retornar código de salida
    if error_count > 0:
        print(f"\n❌ {error_count} casos tienen resultados diferentes entre brute y efficient")
        return 1
    elif failed_count > 0:
        print(f"\n⚠️  {failed_count} casos fallaron en ejecución")
        return 1
    else:
        print(f"\n✅ ¡Validación completada exitosamente!")
        return 0

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Cancelado por el usuario")
        sys.exit(130)