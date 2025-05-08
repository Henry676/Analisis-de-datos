import re
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Dict, Any
from text_extractor import get_optimal_workers

def clean_text(text: str) -> str:
    """Limpia el texto eliminando caracteres especiales y espacios redundantes"""
    text = re.sub(r'[^\w\s.,;!?]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def find_phrase_in_chunk(text: str, phrase: str) -> List[Dict[str, Any]]:
    """
    Busca coincidencias exactas de la frase en un chunk de texto.
    Devuelve las oraciones que contienen la frase con sus posiciones.
    """
    clean_phrase = ' '.join(clean_text(phrase).split())
    if not clean_phrase:
        return []

    pattern = re.compile(r'\b' + re.escape(clean_phrase) + r'\b', flags=re.IGNORECASE)
    sentences = []
    current_start = 0
    
    for i, char in enumerate(text):
        if char == '.' and (i == len(text)-1 or text[i+1] in (' ', '\n', '\r')):
            sentence = text[current_start:i+1].strip()
            if sentence:
                sentences.append(sentence)
            current_start = i + 1

    if not sentences:
        sentences = [text.strip()] if text.strip() else []

    matches = []
    for sentence in sentences:
        found = list(pattern.finditer(sentence))
        if found:
            matches.append({
                'paragraph': sentence,
                'count': len(found),
                'positions': [m.start() for m in found]
            })
    
    return matches

def process_chunk_search(chunk: Tuple[int, int, str], phrase: str) -> Tuple[int, List[Dict[str, Any]]]:
    """
    Procesa un chunk de páginas (inicio, fin, texto).
    Devuelve (total_palabras, coincidencias) para el chunk.
    """
    start_page, end_page, text = chunk
    cleaned_text = clean_text(text)
    word_count = len(cleaned_text.split())
    matches = find_phrase_in_chunk(cleaned_text, phrase)
    
    # Añadir metadata del rango de páginas
    for match in matches:
        match['page_range'] = f"{start_page}-{end_page}"
        match['pages'] = (start_page, end_page)
    
    return word_count, matches

def concurrent_search(page_chunks: List[Tuple[int, int, str]], phrase: str) -> Tuple[int, List[Dict[str, Any]]] :
    total_words = 0
    all_matches = []
    
    max_workers = get_optimal_workers()  
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_chunk_search, chunk, phrase)
            for chunk in page_chunks
        ]
        
        for future in futures:
            chunk_words, chunk_matches = future.result()
            total_words += chunk_words
            all_matches.extend(chunk_matches)
    
    return total_words, all_matches

def find_flexible_phrase(text: str, phrase: str, max_intermediate: int = 2) -> List[Dict[str, Any]]:
    """
    Busca frases flexibles con hasta 2 palabras intermedias entre cada palabra de la frase,
    excluyendo las coincidencias exactas.
    """
    cleaned_text = clean_text(text.lower())
    phrase_words = [w.lower() for w in phrase.split()]
    
    if len(phrase_words) < 2:
        print("La frase debe contener al menos dos palabras.")
        return []
    
    # Construir patrón regex flexible que excluya coincidencias exactas
    pattern_parts = []
    for i, word in enumerate(phrase_words):
        if i > 0:
            pattern_parts.append(r'(?:\W+\w+){1,' + str(max_intermediate) + r'}\W+')
        pattern_parts.append(re.escape(word))
    
    # Unir el patrón completo
    full_pattern = r'\b' + ''.join(pattern_parts) + r'\b'
    pattern = re.compile(full_pattern, flags=re.IGNORECASE)
    
    # Buscar coincidencias con contexto
    matches = []
    for match in pattern.finditer(cleaned_text):
        # Verificar que no sea coincidencia exacta
        matched_text = match.group()
        if matched_text.lower() != phrase.lower():
            start_pos = max(0, match.start() - 50)  # 50 caracteres antes
            end_pos = min(len(cleaned_text), match.end() + 50)  # 50 caracteres después
            
            context = cleaned_text[start_pos:end_pos]
            if start_pos > 0:
                context = "..." + context
            if end_pos < len(cleaned_text):
                context = context + "..."
            
            matches.append({
                'paragraph': context,
                'original': matched_text,
                'count': 1,
                'positions': [match.start() - start_pos]
            })
    
    return matches

def process_flexible_search(chunk: Tuple[int, int, str], phrase: str) -> Tuple[int, List[Dict[str, Any]]]:
    """Procesa un chunk para búsqueda flexible"""
    start_page, end_page, text = chunk
    word_count = len(clean_text(text).split())
    matches = find_flexible_phrase(text, phrase)
    
    for match in matches:
        match['page_range'] = f"{start_page}-{end_page}"
        match['pages'] = (start_page, end_page)
    
    return word_count, matches

def flexible_search(page_chunks: List[Tuple[int, int, str]], phrase: str) -> Tuple[int, List[Dict[str, Any]]]:
    """Búsqueda concurrente flexible"""
    total_words = 0
    all_matches = []
    
    max_workers = get_optimal_workers()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_flexible_search, chunk, phrase)
            for chunk in page_chunks
        ]
        
        for future in futures:
            chunk_words, chunk_matches = future.result()
            total_words += chunk_words
            all_matches.extend(chunk_matches)
    
    return total_words, all_matches