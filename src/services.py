# app/services.py
import io
import base64
import subprocess
import tempfile
from pdf2image import convert_from_bytes, convert_from_path
from pdflatex import PDFLaTeX
from latex import build_pdf
import os
 
 
#using pdf latex - from pdflatex import PDFLaTeX
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
    
# using with subprocess 
def generate_pdf_from_latex_with_subprocess(latex_code: str) -> None:
    pdflatex_path: str = '/Library/TeX/texbin/pdflatex'
    
    pdflatex_command = "pdflatex"
    if not os.path.isfile(pdflatex_path):
        raise FileNotFoundError(f"{pdflatex_path} does not exist.")
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_latex_file = os.path.join(temp_dir, "temp.tex")
            temp_pdf_file = os.path.join(temp_dir, "temp.pdf")
            with open(temp_latex_file, 'w') as f:
                f.write(latex_code)

            # Run pdflatex to generate the PDF
            subprocess.run([pdflatex_path, "-output-directory",
                           temp_dir, temp_latex_file], check=True)
            
             # Read the PDF file as bytes
            with open(temp_pdf_file, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()
                
                
            images = convert_from_bytes(pdf_bytes)
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
        print("An unexpected error occurred: {e}")
        raise
    



#without subprocess sservices 
def generate_pdf_from_latex_without_subprocess(latex_code: str) -> list[bytes]:
    try:
   
        pdf = build_pdf(latex_code)
        images = convert_from_bytes(pdf.data)
        image_bytes_list = []
        for image in images:
            image_byte_arr = io.BytesIO()
            image.save(image_byte_arr, format='PNG')
            image_bytes_list.append(image_byte_arr.getvalue())

        return image_bytes_list

    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")