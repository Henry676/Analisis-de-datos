from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
from typing import List, Dict, Any

def create_exact_search_pdf_report(total_words: int, 
                                 matches: List[Dict[str, Any]], 
                                 phrase: str,
                                 output_file: str = "exact_search_report.pdf") -> str:
    """
    Genera un reporte PDF para búsqueda exacta con el mismo estilo que los otros reportes.
    """
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Estilos personalizados (consistentes con los otros reportes)
    highlight_style = ParagraphStyle(
        'Highlight',
        parent=styles['BodyText'],
        backColor=colors.yellow,
        borderPadding=(2, 2, 2, 2),
        leading=14
    )
    
    story = []
    
    # Título
    story.append(Paragraph("REPORTE DE BÚSQUEDA EXACTA", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    # Información general
    story.append(Paragraph(f"<b>Frase buscada:</b> {phrase}", styles['BodyText']))
    story.append(Paragraph(f"<b>Total de palabras analizadas:</b> {total_words:,}", styles['BodyText']))
    story.append(Paragraph(f"<b>Total de coincidencias:</b> {sum(m['count'] for m in matches)}", styles['BodyText']))
    story.append(Spacer(1, 24))
    
    # Detalle de coincidencias
    if not matches:
        story.append(Paragraph("No se encontraron coincidencias exactas.", styles['BodyText']))
    else:
        story.append(Paragraph("<b>DETALLE DE COINCIDENCIAS</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        for i, match in enumerate(matches, start=1):
            story.append(Paragraph(f"<b>Coincidencia #{i}</b>", styles['BodyText']))
            page_info = match.get('page_range', match.get('page', 'N/A'))
            story.append(Paragraph(f"<b>Página(s):</b> {page_info}", styles['BodyText']))
            story.append(Spacer(1, 6))
            
            # Mostrar contexto con frase resaltada
            paragraph = match.get('paragraph', '')
            if paragraph:
                story.append(Paragraph("<b>Contexto:</b>", styles['BodyText']))
                # Resaltar todas las ocurrencias de la frase
                parts = paragraph.split(phrase)
                for j, part in enumerate(parts):
                    story.append(Paragraph(part, styles['BodyText']))
                    if j < len(parts) - 1:
                        story.append(Paragraph(phrase, highlight_style))
            
            story.append(Spacer(1, 12))
    
    doc.build(story)
    return output_file

def create_flexible_pdf_report(total_words: int, 
                             matches: List[Dict[str, Any]], 
                             phrase: str,
                             output_file: str = "flexible_search_report.pdf") -> str:
    """
    Genera un reporte PDF con las frases flexibles encontradas, resaltando las coincidencias.
    """
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    highlight_style = ParagraphStyle(
        'Highlight',
        parent=styles['BodyText'],
        backColor=colors.yellow,
        borderPadding=(2, 2, 2, 2),
        leading=14
    )
    
    phrase_style = ParagraphStyle(
        'PhraseStyle',
        parent=styles['BodyText'],
        textColor=colors.red,
        backColor=colors.lightgrey,
        borderPadding=(2, 2, 2, 2)
    )
    
    story = []
    
    # Título
    story.append(Paragraph("REPORTE DE BÚSQUEDA FLEXIBLE", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    # Información general
    story.append(Paragraph(f"<b>Frase buscada:</b> {phrase}", styles['BodyText']))
    story.append(Paragraph(f"<b>Total de palabras analizadas:</b> {total_words:,}", styles['BodyText']))
    story.append(Paragraph(f"<b>Total de coincidencias:</b> {sum(m['count'] for m in matches)}", styles['BodyText']))
    story.append(Paragraph("<i>(Coincidencias con hasta 3 palabras intermedias entre términos)</i>", styles['Italic']))
    story.append(Spacer(1, 24))
    
    # Detalle de coincidencias
    if not matches:
        story.append(Paragraph("No se encontraron coincidencias.", styles['BodyText']))
    else:
        story.append(Paragraph("<b>DETALLE DE COINCIDENCIAS</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        for i, match in enumerate(matches, start=1):
            # Encabezado de coincidencia
            story.append(Paragraph(f"<b>Coincidencia #{i}</b>", styles['BodyText']))
            page_info = match.get('page_range', match.get('page', 'N/A'))
            story.append(Paragraph(f"<b>Página(s):</b> {page_info}", styles['BodyText']))
            story.append(Spacer(1, 6))
            
            # Mostrar frase original encontrada
            matched_text = match.get('original', '')
            story.append(Paragraph("<b>Frase encontrada:</b>", styles['BodyText']))
            story.append(Paragraph(matched_text, phrase_style))
            story.append(Spacer(1, 6))
            
            # Mostrar contexto
            paragraph = match.get('paragraph', '')
            if paragraph:
                story.append(Paragraph("<b>Contexto:</b>", styles['BodyText']))
                # Resaltar la coincidencia en el contexto
                start_idx = paragraph.lower().find(matched_text.lower())
                if start_idx != -1:
                    before = paragraph[:start_idx]
                    during = paragraph[start_idx:start_idx+len(matched_text)]
                    after = paragraph[start_idx+len(matched_text):]
                    
                    story.append(Paragraph(before, styles['BodyText']))
                    story.append(Paragraph(during, highlight_style))
                    story.append(Paragraph(after, styles['BodyText']))
                else:
                    story.append(Paragraph(paragraph, styles['BodyText']))
            
            story.append(Spacer(1, 24))
    
    doc.build(story)
    return output_file

def create_multi_pdf_flexible_report(total_words: int, 
                                   matches: List[Dict[str, Any]], 
                                   phrase: str,
                                   output_file: str = "multi_pdf_flexible_search_report.pdf") -> str:
    """
    Genera un reporte PDF consolidado para búsqueda flexible en múltiples PDFs.
    """
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    highlight_style = ParagraphStyle(
        'Highlight',
        parent=styles['BodyText'],
        backColor=colors.yellow,
        borderPadding=(2, 2, 2, 2),
        leading=14
    )
    
    phrase_style = ParagraphStyle(
        'PhraseStyle',
        parent=styles['BodyText'],
        textColor=colors.red,
        backColor=colors.lightgrey,
        borderPadding=(2, 2, 2, 2)
    )
    
    story = []
    
    # Título
    story.append(Paragraph("REPORTE DE BÚSQUEDA FLEXIBLE EN MÚLTIPLES PDFs", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    # Información general
    story.append(Paragraph(f"<b>Frase buscada:</b> {phrase}", styles['BodyText']))
    story.append(Paragraph(f"<b>Total de archivos analizados:</b> {len({m['pdf_path'] for m in matches})}", styles['BodyText']))
    story.append(Paragraph(f"<b>Total de palabras analizadas:</b> {total_words:,}", styles['BodyText']))
    story.append(Paragraph(f"<b>Total de coincidencias:</b> {sum(m['count'] for m in matches)}", styles['BodyText']))
    story.append(Paragraph("<i>(Coincidencias con hasta 3 palabras intermedias entre términos)</i>", styles['Italic']))
    story.append(Spacer(1, 24))
    
    # Detalle de coincidencias por archivo
    if not matches:
        story.append(Paragraph("No se encontraron coincidencias flexibles en ninguno de los archivos.", styles['BodyText']))
    else:
        # Agrupar coincidencias por archivo PDF
        pdfs = {}
        for match in matches:
            pdf_name = match['pdf_name']
            if pdf_name not in pdfs:
                pdfs[pdf_name] = []
            pdfs[pdf_name].append(match)
        
        for pdf_name, pdf_matches in pdfs.items():
            story.append(Paragraph(f"<b>Archivo:</b> {pdf_name}", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            for i, match in enumerate(pdf_matches, start=1):
                story.append(Paragraph(f"<b>Coincidencia #{i}</b>", styles['BodyText']))
                story.append(Paragraph(f"<b>Página(s):</b> {match.get('page_range', 'N/A')}", styles['BodyText']))
                story.append(Spacer(1, 6))
                
                # Mostrar frase encontrada
                matched_text = match.get('original', '')
                story.append(Paragraph("<b>Frase encontrada:</b>", styles['BodyText']))
                story.append(Paragraph(matched_text, phrase_style))
                story.append(Spacer(1, 6))
                
                # Mostrar contexto con frase resaltada
                paragraph = match.get('paragraph', '')
                if paragraph:
                    story.append(Paragraph("<b>Contexto:</b>", styles['BodyText']))
                    start_idx = paragraph.lower().find(matched_text.lower())
                    if start_idx != -1:
                        before = paragraph[:start_idx]
                        during = paragraph[start_idx:start_idx+len(matched_text)]
                        after = paragraph[start_idx+len(matched_text):]
                        
                        story.append(Paragraph(before, styles['BodyText']))
                        story.append(Paragraph(during, highlight_style))
                        story.append(Paragraph(after, styles['BodyText']))
                    else:
                        story.append(Paragraph(paragraph, styles['BodyText']))
                
                story.append(Spacer(1, 12))
            
            story.append(Spacer(1, 24))
    
    doc.build(story)
    return output_file