from typing import List


class Product:
    id: str
    name: str
    repo: str
    path: str | None
    config: dict[str,str]

    def __init__(self, id: str, name: str, repo: str, path: str = None):
        self.id = id
        self.name = name
        self.repo = repo
        self.path = path


    @staticmethod
    def from_dict(product_data: dict[str,str]):
        return Product(
            product_data.get('id'),
            product_data.get('name'),
            product_data.get('repo'),
            product_data.get('path'),
        )

    
    def to_dict(self) -> dict[str,str]:
        return {
            'id': self.id,
            'name': self.name,
            'repo': self.repo,
            'path': self.path,
        }