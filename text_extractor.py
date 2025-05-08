import os
import PyPDF2
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

def get_optimal_workers():
    """Calcula el número óptimo de hilos basado en los núcleos del CPU."""
    cpu_count = os.cpu_count() or 1  # Default 1 si no se detectan núcleos
    # Usamos el mínimo entre: (núcleos * 2) y 32 para evitar sobrecarga
    return min(cpu_count * 2, 32)  

def extract_pages_range(pdf_path: str, start_page: int, end_page: int) -> Tuple[int, int, str]:
    """Extrae texto de un rango específico de páginas del PDF."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(start_page, min(end_page, len(reader.pages))):
                page_text = reader.pages[page_num].extract_text()
                if page_text:  # Evitar concatenar None
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error procesando páginas {start_page}-{end_page}: {str(e)}")
        text = ""
    return (start_page, end_page, text.strip())

def extract_text_in_chunks(pdf_path: str, chunk_size: int = None) -> List[Tuple[int, int, str]]:
    """Extrae texto del PDF en chunks de forma concurrente, con tamaño de chunk automático."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"El archivo {pdf_path} no existe")

    # Configuración dinámica
    with open(pdf_path, 'rb') as file:
        total_pages = len(PyPDF2.PdfReader(file).pages)
    
    # Tamaño de chunk automático (aprox. 10 páginas por núcleo)
    if chunk_size is None:
        cpu_count = os.cpu_count() or 1
        chunk_size = max(10, total_pages // (cpu_count * 2))
    
    # Generar rangos
    ranges = [
        (start, min(start + chunk_size, total_pages))
        for start in range(0, total_pages, chunk_size)
    ]

    # Configuración de hilos
    max_workers = get_optimal_workers()
    print(f"\nProcesando {total_pages} páginas en {len(ranges)} chunks")
    print(f"Hilos activos: {max_workers} (basado en {os.cpu_count()} núcleos)")

    # Procesamiento paralelo
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(extract_pages_range, pdf_path, start, end)
            for start, end in ranges
        ]
        
        results = []
        for future in futures:
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Error en chunk: {str(e)}")
                continue
        
        return results