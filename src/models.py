from pydantic import BaseModel

class LatexRequest(BaseModel):
    latex_code: str
