import matplotlib.pyplot as plt
import numpy as np
import re
from collections import Counter
import os
from typing import List, Tuple, Dict, Any

def generate_word_frequency_heatmap(pages: List[Tuple[int, str]], 
                                 top_n: int = 20, 
                                 output_file: str = "word_heatmap.png",
                                 min_length: int = 4):
    """
    Genera un mapa de calor de palabras frecuentes (longitud >= min_length)
    
    Args:
        pages: Lista de (número_página, texto)
        top_n: Top N palabras a mostrar
        output_file: Archivo de salida
        min_length: Longitud mínima de palabras a considerar
    """
    # 1. Extraer y filtrar palabras
    all_text = ' '.join([page[1] for page in pages]).lower()
    words = [
        word for word in re.findall(r'\b\w+\b', all_text)
        if len(word) >= min_length and not word.isnumeric()
    ]
    
    # 2. Contar frecuencias
    word_counts = Counter(words)
    top_words = word_counts.most_common(top_n)
    
    if not top_words:
        print("No se encontraron palabras que cumplan los criterios")
        return None
    
    # 3. Preparar datos para el heatmap
    words, counts = zip(*top_words)  # Separar palabras y conteos
    
    # 4. Crear visualización
    plt.figure(figsize=(14, 6))
    plt.imshow([counts], cmap='YlOrRd', aspect='auto')
    
    # 5. Personalización
    plt.colorbar(label='Frecuencia')
    plt.xticks(np.arange(len(words)), words, rotation=45, ha='right')
    plt.yticks([])
    plt.title(f'Top {top_n} Palabras Más Frecuentes (≥{min_length} letras)')
    
    # 6. Añadir valores
    for i, count in enumerate(counts):
        plt.text(i, 0, str(count), ha='center', va='center', 
                color='white' if count > max(counts)*0.7 else 'black')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=120, bbox_inches='tight')
    plt.close()
    
    return os.path.abspath(output_file)

def generate_pdf_frequency_heatmap(search_results: List[Dict[str, Any]],
                                output_file: str = "pdf_heatmap.png"):
    """
    Genera un mapa de calor de frecuencias de coincidencias por PDF.
    
    Args:
        search_results: Resultados de búsqueda flexible de múltiples PDFs
        output_file: Archivo de salida para el heatmap
    """
    # Procesar datos para el heatmap
    pdf_counts = {}
    for result in search_results:
        pdf_name = result['pdf_name']
        if pdf_name not in pdf_counts:
            pdf_counts[pdf_name] = 0
        pdf_counts[pdf_name] += result['count']
    
    if not pdf_counts:
        print("No hay datos para generar el heatmap")
        return None
    
    # Ordenar PDFs por número de coincidencias (descendente)
    sorted_pdfs = sorted(pdf_counts.items(), key=lambda x: x[1], reverse=True)
    pdf_names, counts = zip(*sorted_pdfs)
    counts_matrix = [counts]  # Matriz 1xN para el heatmap
    
    # Crear visualización (manteniendo el mismo estilo)
    plt.figure(figsize=(14, 6))
    heatmap = plt.imshow(counts_matrix, cmap='YlOrRd', aspect='auto')
    
    # Personalización (igual que tu heatmap actual)
    plt.colorbar(heatmap, label='Número de coincidencias')
    plt.xticks(np.arange(len(pdf_names)), pdf_names, rotation=45, ha='right')
    plt.yticks([])
    plt.title('Coincidencias de frases aproximadas por PDF')
    
    # Añadir valores en las celdas
    for i, count in enumerate(counts):
        plt.text(i, 0, str(count), ha='center', va='center', 
                color='white' if count > max(counts)*0.7 else 'black')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=120, bbox_inches='tight')
    plt.close()
    
    return os.path.abspath(output_file)