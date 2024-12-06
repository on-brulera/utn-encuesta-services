import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from application.conn.db import db
from application.estilos.api_v1_0.resources import routes_estilos_v1
from .ext import ma, migrate


def create_app(settings_module):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(settings_module)
    # Inicializa las extensiones
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    # JWT
    SECRET_KEY = os.environ.get("SECRET_KEY") or "this is a secret"
    app.config["SECRET_KEY"] = SECRET_KEY
    # Captura todos los errores 404
    Api(app, catch_all_404s=True)
    # Deshabilita el modo estricto de acabado de una URL con /
    app.url_map.strict_slashes = False
    # Registra los blueprints
    app.register_blueprint(routes_estilos_v1)
    return app
