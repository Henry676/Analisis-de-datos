from text_extractor import extract_text_in_chunks
from search_engine import flexible_search
from pdf_reporter import create_multi_pdf_flexible_report
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Tuple
from text_extractor import get_optimal_workers
from heatmap import generate_pdf_frequency_heatmap


def process_single_pdf_flexible(pdf_path: str, phrase: str) -> Tuple[str, int, List[Dict[str, Any]]]:
    """Procesa un solo PDF con búsqueda flexible y devuelve resultados"""
    if not os.path.exists(pdf_path):
        print(f"\nEl archivo {pdf_path} no existe, omitiendo...")
        return (pdf_path, 0, [])
    
    try:
        print(f"\nProcesando: {os.path.basename(pdf_path)}...")
        page_chunks = extract_text_in_chunks(pdf_path)
        pdf_words, matches = flexible_search(page_chunks, phrase)
        
        # Añadir información del archivo a cada coincidencia
        for match in matches:
            match['pdf_name'] = os.path.basename(pdf_path)
            match['pdf_path'] = pdf_path
        
        print(f"Procesado: {os.path.basename(pdf_path)} - {len(matches)} coincidencias flexibles")
        return (pdf_path, pdf_words, matches)
        
    except Exception as e:
        print(f"Error procesando {pdf_path}: {str(e)}")
        return (pdf_path, 0, [])


def process_multi_pdf_flexible_search(pdf_paths: List[str]):
    phrase = input("Ingrese la frase que desea buscar (puede tener hasta 3 palabras intermedias): ")
    print(f"\nBuscando frase flexible: '{phrase}' en {len(pdf_paths)} archivos PDF...")
    
    start_time = time.time()
    all_results = []
    total_words = 0
    
    # Configurar concurrencia para múltiples PDFs
    max_workers = min(get_optimal_workers(), len(pdf_paths)) if len(pdf_paths) > 1 else 1
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Enviar todos los PDFs a procesar concurrentemente
        futures = {
            executor.submit(process_single_pdf_flexible, pdf_path, phrase): pdf_path 
            for pdf_path in pdf_paths
        }
        
        for future in as_completed(futures):
            pdf_path, pdf_words, matches = future.result()
            total_words += pdf_words
            all_results.extend(matches)
    
    # Generar reportes si hay resultados
    if all_results:
        print("\nGenerando reporte PDF consolidado...")
        report_file = create_multi_pdf_flexible_report(total_words, all_results, phrase)
        
        print("\nGenerando mapa de calor...")
        heatmap_file = generate_pdf_frequency_heatmap(all_results)
        
        print("\n=== RESULTADOS FINALES ===")
        print(f"Tiempo total: {time.time() - start_time:.2f}s")
        print(f"Total de palabras analizadas: {total_words:,}")
        print(f"Total de ocurrencias flexibles de '{phrase}': {sum(m['count'] for m in all_results)}")
        print(f"Reporte PDF generado: {os.path.abspath(report_file)}")
        print(f"Mapa de calor generado: {os.path.abspath(heatmap_file)}")
        
        # Abrir ambos archivos si es posible
        if report_file and os.path.exists(report_file):
            os.system(f'xdg-open "{report_file}"')
        if heatmap_file and os.path.exists(heatmap_file):
            os.system(f'xdg-open "{heatmap_file}"')
    else:
        print("\nNo se encontraron coincidencias flexibles en ninguno de los archivos PDF")