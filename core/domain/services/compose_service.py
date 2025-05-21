import os
import yaml
import subprocess
from core.domain.models.compose_models import ComposeModel

COMPOSE_DIR = r"C:\Users\walte\OneDrive\Escritorio\products-server\repositories\compose"

def generate_compose_file(compose_data: ComposeModel, filename: str) -> str:
    filepath = os.path.join(COMPOSE_DIR, filename)
    data_dict = compose_data.dict(exclude_none=True)
    # No incluimos 'version' para evitar warning
    data_dict.pop('version', None)
    with open(filepath, 'w') as f:
        yaml.dump(data_dict, f, sort_keys=False)
    return filepath

def run_docker_compose(compose_file_path: str) -> (bool, str):
    try:
        result = subprocess.run(
            ["docker-compose", "-f", compose_file_path, "up", "-d", "--build"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr
