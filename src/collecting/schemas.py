from pydantic import BaseModel

class ProductBase(BaseModel):
    product_id: int