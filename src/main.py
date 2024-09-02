
import base64

from fastapi.responses import StreamingResponse
from fastapi import FastAPI, HTTPException

from services import generate_images_from_latex, generate_pdf_from_latex_with_subprocess, generate_pdf_from_latex_without_subprocess
from models import ImageBytes, LatexRequest
from PIL import Image
import io

app = FastAPI()


@app.get('/')
def index():
    return {'hit this url:http://localhost:8000/docs'}


@app.post("/convert-latex/")
async def convert_latex(request: LatexRequest):
    try:
        image_bytes_list = generate_images_from_latex(request.latex_code)
        if image_bytes_list is None:
            raise HTTPException(
                status_code=500, detail="Error generating image bytes.")
        return {"images": image_bytes_list}
    except Exception as e:
        print(f"An error occurred in the API handler: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def bytes_to_image(image_bytes: bytes) -> Image:
    image_stream = io.BytesIO(image_bytes)
    pil_image_object = Image.open(image_stream)
    return pil_image_object


@app.post("/convert-bytes-to-image/")
async def convert_bytes_to_image(image_bytes: ImageBytes):
    try:
        image_data = base64.b64decode(image_bytes.image_data)
        image = bytes_to_image(image_data)
        image_stream = io.BytesIO()
        image.save(image_stream, format='PNG')
        image_stream.seek(0)
        # Return the image as a StreamingResponse
        return StreamingResponse(image_stream, media_type="image/png", headers={"Content-Disposition": "attachment; filename=image.png"})

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to convert image: {str(e)}")


# with subprocess
@app.post("/convert-latex/with_subprocess")
async def convert_latex(request: LatexRequest):
    try:
        image_bytes_list = generate_pdf_from_latex_with_subprocess(
            request.latex_code)
        if image_bytes_list is None:
            raise HTTPException(
                status_code=500, detail="Error generating image bytes.")
        return {"images": image_bytes_list}
    except Exception as e:
        print(f"An error occurred in the API handler: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

## without subprocess 
@app.post("/convert-latex/without_subprocess")
async def convert_latex(request: LatexRequest):
    try:
        image_bytes_list = generate_pdf_from_latex_without_subprocess(
            request.latex_code)
        if image_bytes_list is None:
            raise HTTPException(
                status_code=500, detail="Error generating image bytes.")
        return {"images": image_bytes_list}
    except Exception as e:
        print(f"An error occurred in the API handler: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
