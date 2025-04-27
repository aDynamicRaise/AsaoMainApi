from pydantic import BaseModel

class ProductBase(BaseModel):
    product_id: int

class ProductLink(BaseModel):
    product_link: str
    seller_id: int

