import threading
import subprocess
import os
import time
import re
from typing import Dict
from core.domain.models.image_model import ImageBuildState, BuildStatus

# Ruta absoluta fija para logs
LOGS_DIR = r"C:\Users\walte\OneDrive\Escritorio\products-server\repositories\log"
os.makedirs(LOGS_DIR, exist_ok=True)

# Variable global para mantener estados de builds
build_states: Dict[str, ImageBuildState] = {}

def sanitize_filename(name: str) -> str:
    """
    Reemplaza caracteres inválidos en nombres de archivo de Windows por guion bajo.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def build_image_async(image_name: str, dockerfile_path: str) -> str:
    safe_image_name = sanitize_filename(image_name)
    build_id = f"{safe_image_name}_{int(time.time())}"
    log_file_path = os.path.join(LOGS_DIR, f"{build_id}.log")

    # Registrar estado inicial
    build_states[build_id] = ImageBuildState(
        image_name=image_name,
        status=BuildStatus.RUNNING,
        log_file=log_file_path
    )

    def run_build():
        try:
            with open(log_file_path, 'w', encoding='utf-8') as log_file:
                log_file.write(f"Inició la construcción de la imagen {image_name} a las {time.ctime()}\n")
                log_file.flush()

                cmd = [
                    "docker", "build",
                    "-t", image_name,
                    "-f", dockerfile_path,
                    os.path.dirname(dockerfile_path)
                ]
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in process.stdout:
                    log_file.write(line)
                    log_file.flush()
                process.wait()

                if process.returncode == 0:
                    build_states[build_id].status = BuildStatus.SUCCESS
                    log_file.write(f"\nConstrucción finalizada con éxito a las {time.ctime()}\n")
                else:
                    build_states[build_id].status = BuildStatus.FAILED
                    log_file.write(f"\nConstrucción fallida con código {process.returncode} a las {time.ctime()}\n")
        except Exception as e:
            build_states[build_id].status = BuildStatus.FAILED
            # En caso de error al escribir el log, imprime en consola
            print(f"Error al abrir o escribir el archivo de log: {e}")

    thread = threading.Thread(target=run_build, daemon=True)
    thread.start()

    return build_id
