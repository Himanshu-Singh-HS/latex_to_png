

def generate_images_from_latex(latex_code: str):
    '''
    This function is for converting LaTeX to image (in bytes object).
    
    :param latex_code: Takes LaTeX string as input 
    :return: Returns list of bytes of images
    '''
    try:
        pdfl = PDFLaTeX.from_binarystring(
            latex_code.encode('utf-8'), jobname="temp_job")
        pdf, _, _ = pdfl.create_pdf(keep_pdf_file=False, keep_log_file=False)
        images = convert_from_bytes(pdf)
        image_streams = []
        for image in images:
            image_stream = io.BytesIO()
            image.save(image_stream, format='PNG')
            image_stream.seek(0)
            image_streams.append(image_stream)
        return image_streams

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.post("/convert_latex/")
async def convert_latex(request: LatexRequest):
    try:
        image_streams = generate_images_from_latex(request.latex_code)
        if not image_streams:
            raise HTTPException(status_code=500, detail="Error generating images")
        
        # Respond with the first image for simplicity
        image_stream = image_streams[0]
        return StreamingResponse(image_stream, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
    
    
# import base64
# from fastapi import FastAPI,HTTPException
# import io
# from pdf2image import convert_from_bytes
# from pdflatex import PDFLaTeX
# import io
# from pydantic import BaseModel

# app = FastAPI()



# @app.get('/')
# def index():
#     return {'yes api is working'}

# class LatexRequest(BaseModel):
#     latex_code: str

# def generate_images_from_latex(latex_code: str):
#     '''
#     This function is for converting LaTeX to images (in bytes objects).
    
#     :param latex_code: Takes LaTeX string as input 
#     :return: Returns list of bytes of images
#     '''
#     try:
#         pdfl = PDFLaTeX.from_binarystring(
#             latex_code.encode('utf-8'), jobname="temp_job")
#         pdf, _, _ = pdfl.create_pdf(keep_pdf_file=False, keep_log_file=False)
#         images = convert_from_bytes(pdf)
#         image_bytes_list = []
#         for image in images:
#             image_stream = io.BytesIO()
#             image.save(image_stream, format='PNG')
#             image_bytes = image_stream.getvalue()
#             image_base64 = base64.b64encode(image_bytes).decode('utf-8')
#             image_bytes_list.append(image_base64)
#         return image_bytes_list

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

# @app.post("/convert-latex/")
# async def convert_latex(request: LatexRequest):
#     try:
#         image_bytes_list = generate_images_from_latex(request.latex_code)
#         if image_bytes_list is None:
#             raise HTTPException(status_code=500, detail="Error generating images bytes ")
        
#         return {"images": image_bytes_list}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))




