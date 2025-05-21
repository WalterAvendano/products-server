from pydantic import BaseModel
from typing import Optional, List, Dict

class ServiceModel(BaseModel):
    image: Optional[str] = None
    depends_on: Optional[List[str]] = None
    ports: Optional[List[str]] = None
    volumes: Optional[List[str]] = None
    environment: Optional[List[str]] = None  # Lista de strings "KEY=VALUE"
    restart: Optional[str] = None

class ComposeModel(BaseModel):
    services: Dict[str, ServiceModel]
    volumes: Optional[Dict[str, dict]] = None
