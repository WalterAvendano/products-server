from flask import Flask
import os
from infrastructure.api.controllers.products import products

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        FLASK_ENV='debug'
    )

    # a simple page that says hello
    app.register_blueprint(products)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app