from abc import ABC, abstractmethod
from typing import List
from core.domain.models.products import Product


class ProductRepository(ABC):
    @abstractmethod
    def find_one(self, product_id: str) -> Product:
        pass

    @abstractmethod
    def find(self, page:int=None, size:int=None) -> List[Product]:
        pass
    
    @abstractmethod
    def create(self, product: Product):
        pass

    @abstractmethod
    def delete(self, product_id: str):
        pass