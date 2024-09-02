from pydantic import BaseModel

class LatexRequest(BaseModel):
    latex_code: str

class ImageBytes(BaseModel):
    image_data: str