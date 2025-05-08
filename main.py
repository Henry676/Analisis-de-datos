from text_extractor import extract_text_in_chunks
from search_engine import concurrent_search, flexible_search
from user import get_user_choice, get_search_phrase, get_pdf_path
from heatmap import generate_word_frequency_heatmap
from multi_pdf_searcher import process_multi_pdf_flexible_search
from user import get_user_choice, get_search_phrase, get_pdf_path, get_multiple_pdf_paths

import os
import time

from pdf_reporter import create_exact_search_pdf_report

def process_exact_search(page_chunks, pages):
    phrase = get_search_phrase("Ingrese la frase exacta que desea buscar: ")
    print(f"\nBuscando frase exacta: '{phrase}'...")
    start_time = time.time()
    total_words, matches = concurrent_search(page_chunks, phrase)
    
    print("Generando reporte PDF...")
    report_file = create_exact_search_pdf_report(total_words, matches, phrase)
    
    print("\n=== RESULTADOS ===")
    print(f"Tiempo: {time.time() - start_time:.2f}s")
    print(f"Palabras analizadas: {total_words:,}")
    print(f"Ocurrencias de '{phrase}': {sum(m['count'] for m in matches)}")
    print(f"Reporte PDF generado: {os.path.abspath(report_file)}")
    
    # Abrir el PDF automáticamente si es posible
    if report_file and os.path.exists(report_file):
        os.system(f'xdg-open "{report_file}"')

def process_heatmap(pages):
    print("\nGenerando mapa de calor...")
    start_time = time.time()
    heatmap_file = generate_word_frequency_heatmap(
        pages, 
        top_n=15,
        min_length=4
    )
    
    print("\n=== RESULTADOS ===")
    print(f"Tiempo: {time.time() - start_time:.2f}s")
    print(f"Heatmap: {os.path.abspath(heatmap_file) if heatmap_file else 'No generado'}")
    
    if heatmap_file and os.path.exists(heatmap_file):
        os.system(f'xdg-open "{heatmap_file}"')

from pdf_reporter import create_flexible_pdf_report

def process_flexible_search(page_chunks, pages):
    phrase = get_search_phrase("Ingrese la frase que desea buscar (puede tener hasta 3 palabras intermedias entre términos): ")
    print(f"\nBuscando frase flexible: '{phrase}'...")
    start_time = time.time()
    total_words, matches = flexible_search(page_chunks, phrase)
    
    print("Generando reporte PDF...")
    report_file = create_flexible_pdf_report(total_words, matches, phrase)
    
    print("\n=== RESULTADOS ===")
    print(f"Tiempo: {time.time() - start_time:.2f}s")
    print(f"Palabras analizadas: {total_words:,}")
    print(f"Ocurrencias flexibles de '{phrase}': {sum(m['count'] for m in matches)}")
    print(f"Reporte PDF generado: {os.path.abspath(report_file)}")
    
    if report_file and os.path.exists(report_file):
        os.system(f'xdg-open "{report_file}"')


def main():
    pdf_path = get_pdf_path()
    
    # Extraer texto una sola vez al inicio
    print("\n=== Procesando libro (esto puede tomar unos segundos)... ===")
    page_chunks = extract_text_in_chunks(pdf_path)
    pages = [(chunk[0], chunk[2]) for chunk in page_chunks]
    print("=== Libro procesado y listo para búsquedas ===")
    
    while True:
        choice = get_user_choice()
        
        if choice == "1":
            process_exact_search(page_chunks, pages)
        elif choice == "2":
            process_flexible_search(page_chunks, pages)
        elif choice == "3":
            process_heatmap(pages)
        elif choice == "4":
            pdf_paths = get_multiple_pdf_paths()
            process_multi_pdf_flexible_search(pdf_paths)
        elif choice == "5":
            print("\nSaliendo del programa...")
            break
        else:
            print("\nOpción no válida. Por favor, seleccione 1-5.")
if __name__ == "__main__":
    main()