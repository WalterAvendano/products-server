from flask import Blueprint, request, jsonify
from core.domain.models.compose_models import ComposeModel
from core.domain.services.compose_service import generate_compose_file, run_docker_compose
import uuid

compose_blueprint = Blueprint('compose', __name__)

@compose_blueprint.route('/create', methods=['POST'])
def create_compose():
    try:
        data = request.get_json()

        compose_name = data.pop('compose_name', None)
        if compose_name:
            filename = f"{compose_name}.yml"
        else:
            filename = f"docker-compose-{uuid.uuid4().hex}.yml"

        compose_model = ComposeModel(**data)

        filepath = generate_compose_file(compose_model, filename)

        success, message = run_docker_compose(filepath)
        if success:
            return jsonify({
                "message": "Servicios levantados correctamente con docker-compose",
                "compose_file": filename,
                "docker_compose_output": message
            }), 200
        else:
            return jsonify({
                "error": "Error al levantar servicios con docker-compose",
                "details": message
            }), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400
