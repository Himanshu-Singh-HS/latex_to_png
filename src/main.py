from fastapi import FastAPI, HTTPException
from services import generate_images_from_latex 
from models import LatexRequest
app = FastAPI()

@app.post("/convert-latex/")
async def convert_latex(request: LatexRequest):
    try:
        image_bytes_list = generate_images_from_latex(request.latex_code)
        if image_bytes_list is None:
            raise HTTPException(status_code=500, detail="Error generating image bytes.")
        return {"images": image_bytes_list}
    except Exception as e:
        print(f"An error occurred in the API handler: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
