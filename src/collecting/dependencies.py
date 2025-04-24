from .repositories import ProductRepository
from .services import ProductService


def product_service():
    return ProductService(ProductRepository)