from pydantic import BaseModel

class BagCreate(BaseModel):
    name: str
    brand: str
    price: int

class BagResponse(BaseModel):
    id: str
    name: str
    brand: str
    price: int

    class Config:
        from_attributes = True
