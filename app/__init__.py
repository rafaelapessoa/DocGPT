from flask import Flask
from app.routes.document_routes import document_routes

def create_app():
    app = Flask(__name__)

    # Registrar rutas de documentos
    app.register_blueprint(document_routes)

    return app
