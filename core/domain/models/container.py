from typing import List


class Container:
    image_name: str
    submodules: List[str]
    env: str
    config: dict[str,str]

    def __init__(self, image: str, submodules: List[str], 
                env: str, config: dict[str,str]):
        self.image_name = image
        self.submodules = submodules
        self.env = env
        self.config = config


    @staticmethod
    def from_dict(container_data: dict[str,str]):
        return Container(
            container_data.get('image'),
            container_data.get('submodules'),
            container_data.get('env'),
            container_data.get('config'),
        )

    
    def to_dict(self) -> dict[str,str]:
        return {
            'image': self.image_name,
            'submodules': self.submodules,
            'env': self.env,
            'config': self.config,
        }