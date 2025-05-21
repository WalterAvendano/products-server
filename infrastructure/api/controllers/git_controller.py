from flask import Blueprint, request, jsonify
from core.domain.services.git_service import GitService

git_blueprint = Blueprint('git', __name__)
mongo = None  # Se asignará desde app.py

@git_blueprint.route('/clone', methods=['POST'])
def clone_repository():
    data = request.get_json()
    repo_url = data.get('repo_url')
    repo_name = data.get('repo_name')
    branch = data.get('branch')

    if not repo_url:
        return jsonify({"error": "Falta el parámetro 'repo_url'"}), 400

    try:
        result = GitService.clone_repository_with_submodules(
            repo_url=repo_url,
            repo_name=repo_name,
            branch=branch
        )
        # Guardar en MongoDB
        git_blueprint.mongo.db.submodules.insert_one(result)

        return jsonify({
            "message": "Repositorio clonado exitosamente con submódulos",
            "repository": result
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
