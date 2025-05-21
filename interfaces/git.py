from abc import ABC, abstractmethod
from core.domain.models.products import Product
from git import Repo


class GitAdapter(ABC):
    @abstractmethod
    def clone(self, product: Product):
        pass

    
    def update(self, product_id: str):
        pass

class GitCore:
    def generate_path(self, path: str, repo: str) -> str:
        # https://github.com/user/repo.git
        # or git@github.com:user/repo.git
        # The first split will always leave the repo name at
        # the last element and the second one will only take the name
        # excluding the git part.
        project_name = repo.split('/')[:-1].split('.')[0]
        return f'{path}/{project_name}'


class GitAdapterImplementation(GitAdapter):
    core: GitCore
    path: str

    def __init__(self, git_core: GitCore, path: str = './repositories/'):
        self.core = git_core
        self.path = path

    def clone(self, product: Product):
        full_path = self.core.generate_path(self.path, product.repo)
        product.path = full_path
        repo = Repo.clone_from(product.url, product.path)
        return {'success': True}