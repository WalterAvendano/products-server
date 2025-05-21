from pydantic import BaseModel
from enum import Enum

class BuildStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

class ImageBuildRequest(BaseModel):
    image_name: str
    dockerfile_name: str

class ImageBuildState(BaseModel):
    image_name: str
    status: BuildStatus
    log_file: str  # Ruta al archivo de log

