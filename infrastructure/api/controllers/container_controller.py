from flask import Blueprint, request, jsonify
from core.domain.services.container_service import ContainerService

container_blueprint = Blueprint('container', __name__)
mongo = None  # Se asigna desde app.py

@container_blueprint.route('/list', methods=['GET'])
def list_containers():
    all_param = request.args.get('all', 'false').lower() == 'true'
    try:
        containers = ContainerService.list_containers(all_containers=all_param)
        return jsonify(containers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@container_blueprint.route('/pause', methods=['POST'])
def pause_container():
    data = request.get_json()
    container_id = data.get('container_id') or data.get('container_name')
    if not container_id:
        return jsonify({"error": "Falta 'container_id' o 'container_name'"}), 400
    try:
        result = ContainerService.pause_container(container_id)
        return jsonify({"message": "Contenedor pausado", "container": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@container_blueprint.route('/unpause', methods=['POST'])
def unpause_container():
    data = request.get_json()
    container_id = data.get('container_id') or data.get('container_name')
    if not container_id:
        return jsonify({"error": "Falta 'container_id' o 'container_name'"}), 400
    try:
        result = ContainerService.unpause_container(container_id)
        return jsonify({"message": "Contenedor reanudado", "container": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@container_blueprint.route('/remove', methods=['DELETE'])
def remove_container():
    data = request.get_json()
    container_id = data.get('container_id') or data.get('container_name')
    if not container_id:
        return jsonify({"error": "Falta 'container_id' o 'container_name'"}), 400
    try:
        result = ContainerService.remove_container(container_id)
        return jsonify({"message": "Contenedor eliminado", "container": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@container_blueprint.route('/create', methods=['POST'])
def create_container():
    data = request.get_json()
    image_name = data.get('image_name')
    container_name = data.get('container_name')

    if not image_name:
        return jsonify({"error": "Falta el parámetro 'image_name'"}), 400

    try:
        result = ContainerService.create_container(image_name=image_name, container_name=container_name)
        return jsonify({"message": "Contenedor creado", "container": result}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

