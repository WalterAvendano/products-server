from flask import Blueprint, request, jsonify
from core.domain.models.dockerfile_models import OdooDockerfile, GenericDockerfile, DockerfileService
import os

dockerfile_blueprint = Blueprint('dockerfile', __name__)

# La instancia mongo se asigna desde app.py
mongo = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DOCKERFILES_PATH = os.path.join(BASE_DIR, 'repositories', 'dockerfiles')

@dockerfile_blueprint.route('/odoo', methods=['POST'])
def generate_odoo_dockerfile():
    data = request.get_json()
    try:
        odoo_data = OdooDockerfile(**data)
        content = DockerfileService.build_odoo_dockerfile(odoo_data)

        file_path = os.path.join(DOCKERFILES_PATH, odoo_data.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Asegura carpeta

        with open(file_path, 'w') as f:
            f.write(content)

        dockerfile_blueprint.mongo.db.dockerfiles.insert_one(odoo_data.dict() | {"content": content})

        return jsonify({"message": "Dockerfile Odoo generado y guardado", "filename": odoo_data.filename}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@dockerfile_blueprint.route('/generic', methods=['POST'])
def generate_generic_dockerfile():
    data = request.get_json()
    try:
        generic_data = GenericDockerfile(**data)
        content = DockerfileService.build_generic_dockerfile(generic_data)

        file_path = os.path.join(DOCKERFILES_PATH, generic_data.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            f.write(content)

        dockerfile_blueprint.mongo.db.dockerfiles.insert_one(generic_data.dict() | {"content": content})

        return jsonify({"message": "Dockerfile genérico generado y guardado", "filename": generic_data.filename}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@dockerfile_blueprint.route('/list', methods=['GET'])
def list_dockerfiles():
    try:
        dockerfiles = list(dockerfile_blueprint.mongo.db.dockerfiles.find({}, {"_id": 0}))
        return jsonify(dockerfiles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

