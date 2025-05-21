from flask import Blueprint, request, jsonify
from core.domain.models.image_model import ImageBuildRequest
from core.domain.services.image_service import build_image_async, build_states
import os

image_blueprint = Blueprint('image', __name__)

@image_blueprint.route('/build', methods=['POST'])
def build_image():
    data = request.get_json()
    try:
        build_req = ImageBuildRequest(**data)
        dockerfile_path = os.path.join('repositories', 'dockerfiles', build_req.dockerfile_name)
        if not os.path.isfile(dockerfile_path):
            return jsonify({"error": "Dockerfile no encontrado"}), 404

        build_id = build_image_async(build_req.image_name, dockerfile_path)

        return jsonify({"message": "Comenzó el proceso de construcción", "build_id": build_id}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@image_blueprint.route('/build/status/<build_id>', methods=['GET'])
def build_status(build_id):
    state = build_states.get(build_id)
    if not state:
        return jsonify({"error": "Build ID no encontrado"}), 404
    return jsonify({
        "image_name": state.image_name,
        "status": state.status,
        "log_file": state.log_file
    })
