from io import BytesIO
from PIL import Image
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
import uuid

app = FastAPI()

 
IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'images')

 
os.makedirs(IMAGE_DIR, exist_ok=True)

class ImageBytes(BaseModel):
    image_data: bytes

def bytes_to_image(image_bytes: bytes) -> Image:
    return Image.open(BytesIO(image_bytes))

# @app.post("/convert-bytes/")
async def convert_bytes_to_image(request: Request):
    try:
        
        raw_body = await request.body()
        image_data = raw_body
        
        
        image = bytes_to_image(image_data)
        
       
        image_filename = f"temp_{uuid.uuid4().hex[:5]}.png"
        output_image_path = os.path.join(IMAGE_DIR, image_filename)
         
        image.save(output_image_path)
        
       
        image_url = f"/images/{image_filename}"
        
        return {"message": "Image converted and saved successfully.", "image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to convert image: {str(e)}")

convert_bytes_to_image(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00d\x08\x02\x00\x00\x00\xff\x80\x02\x03\x00\x00\x00\xe6IDATx\x9c\xed\xd0A\t\x00 \x00\xc0@\xb5\x7fg\xad\xe0^"\xdc%\x18\x9b{pk\xbd\x0e\xf8\x89Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\x81Y\xc1\x01\x8a^\x01\xc7\xf1\x84\x1az\x00\x00\x00\x00IEND\xaeB`\x82'
)