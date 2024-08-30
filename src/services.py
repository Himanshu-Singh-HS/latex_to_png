# app/services.py
import io
import base64
from pdf2image import convert_from_bytes
from pdflatex import PDFLaTeX

def generate_images_from_latex(latex_code: str):
    '''
    Converts LaTeX to images (in bytes objects).
    
    :param latex_code: Takes LaTeX string as input 
    :return: List of base64-encoded image strings
    '''
    try:
        pdfl = PDFLaTeX.from_binarystring(
            latex_code.encode('utf-8'), jobname="temp_job")
        pdf, _, _ = pdfl.create_pdf(keep_pdf_file=False, keep_log_file=False)
        images = convert_from_bytes(pdf)
        image_bytes_list = []
        for image in images:
            image_stream = io.BytesIO()
            image.save(image_stream, format='PNG')
            image_bytes = image_stream.getvalue()
            # Encode image bytes to base64
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            image_bytes_list.append(image_base64)
        return image_bytes_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
