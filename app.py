from flask import Flask, jsonify
from flask_pymongo import PyMongo

# Importa los blueprints de tus controladores
from infrastructure.api.controllers.dockerfile_controller import dockerfile_blueprint
from infrastructure.api.controllers.image_controller import image_blueprint
from infrastructure.api.controllers.container_controller import container_blueprint
from infrastructure.api.controllers.git_controller import git_blueprint
from infrastructure.api.controllers.compose_controller import compose_blueprint  # Importa el nuevo blueprint


app = Flask(__name__)

# Configuración de la conexión a MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/git_clones"
mongo = PyMongo(app)

# Asignar la instancia de mongo a los blueprints que la usan
dockerfile_blueprint.mongo = mongo
# Si image_blueprint usa mongo, asigna también:
# image_blueprint.mongo = mongo
container_blueprint.mongo = mongo
git_blueprint.mongo = mongo

# Registrar los blueprints con sus prefijos de URL
app.register_blueprint(dockerfile_blueprint, url_prefix='/dockerfile')
app.register_blueprint(image_blueprint, url_prefix='/images')
app.register_blueprint(container_blueprint, url_prefix='/containers')
app.register_blueprint(git_blueprint, url_prefix='/git')
app.register_blueprint(compose_blueprint, url_prefix='/compose')  # Registro del nuevo blueprint


# Ruta principal de la API
@app.route('/')
def home():
    return jsonify({
        "message": "API para Dockerfiles, imágenes, contenedores y repositorios git",
        "endpoints": {
            "POST /dockerfile/odoo": "Genera Dockerfile para Odoo y lo guarda",
            "POST /dockerfile/generic": "Genera Dockerfile genérico y lo guarda",
            "GET /dockerfile/list": "Lista Dockerfiles guardados",
            "POST /images/build": "Construye una imagen Docker desde un Dockerfile",
            "GET /images/build/status/<build_id>": "Consulta el estado de la construcción de la imagen",
            "POST /containers/create": "Crea un contenedor desde una imagen existente",
            "POST /git/clone": "Clona un repositorio con submódulos",
            "POST /compose/create": "Crea y levanta contenedores dinámicamente con docker-compose"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
