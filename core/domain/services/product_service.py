from abc import ABC, abstractmethod
from typing import List
from core.domain.models.products import Product
from application.ports.product_port import ProductRepository
from interfaces.git import GitAdapter

class ProductsService(ABC):
    @abstractmethod
    def create_product(self, product: Product):
        pass
    

    @abstractmethod
    def find_product(self, product_id: str) -> Product:
        pass
    

    @abstractmethod
    def find_products(self, page:int = None, size:int=None) -> List[Product]:
        pass
    
    
    @abstractmethod
    def delete_product(self, product_id: str) -> Product:
        pass


class ProductServiceImplementation(ProductsService):
    _product_repository: ProductRepository
    _git_adapter: GitAdapter

    def __init__(self, product_repository: ProductRepository, git_adapter: GitAdapter):
        self._product_repository = product_repository
        self._git_adapter = git_adapter

    
    def create_product(self, product: Product):
        # clone repository
        result = self._git_adapter.clone(product)
        if not result['success']:
            return {'success': False}
        # store path
        self._product_repository.create(product)
        return {'success': True}
    

    def find_products(self, page: int = None, size: int = None) -> List[Product]:
        products = self._product_repository.find()
        return products