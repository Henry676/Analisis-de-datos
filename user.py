import subprocess
import os

def get_multiple_pdf_paths():
    """Abre el explorador de archivos para seleccionar múltiples PDFs usando zenity"""
    try:
        # Ejecutar zenity para seleccionar archivos
        result = subprocess.run([
            'zenity', '--file-selection',
            '--title=Seleccione archivos PDF a analizar',
            '--file-filter=Archivos PDF | *.pdf',
            '--multiple',
            '--separator=\n'
        ], capture_output=True, text=True, check=True)
        
        # Procesar los archivos seleccionados
        if result.stdout:
            paths = result.stdout.strip().split('\n')
            return [path for path in paths if path.endswith('.pdf')]
        
    except subprocess.CalledProcessError:
        # El usuario canceló la selección
        pass
    except Exception as e:
        print(f"Error al seleccionar archivos: {str(e)}")
    
    return []

def get_user_choice():
    print("\nOpciones disponibles:")
    print("1. Buscar frase exacta (un PDF)")
    print("2. Buscar frases aproximadas (hasta 3 palabras intermedias)")
    print("3. Generar mapa de calor de palabras frecuentes")
    print("4. Buscar frase aproximada en múltiples PDFs")
    print("5. Salir")
    return input("Seleccione una opción (1-5): ").strip()

def get_multiple_phrases():
    print("\nIngrese las frases que desea buscar (una por línea). Vacío para terminar):")
    frases = []
    while True:
        frase = input(f"Frase {len(frases)+1}: ").strip()
        if not frase:
            if not frases:
                print("Debe ingresar al menos una frase")
                continue
            break
        frases.append(frase)
    return frases

def get_search_phrase(prompt):
    return input(prompt).strip()

def get_pdf_path():
    return "/home/hertz676/Documentos/Analisis 2do parcial/Dracula.pdf".strip()