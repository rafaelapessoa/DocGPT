import pytest
import os
import io
from app.models.file_manager import FileManager
from app.routes.document_routes import document_routes, documents_db
from flask import Flask

# Configuración para preparar y limpiar el entorno de pruebas
def setup_function():
    os.makedirs("./app/uploads", exist_ok=True)

def teardown_function():
    if os.path.exists("./app/uploads/valid_file.txt"):
        os.remove("./app/uploads/valid_file.txt")

# Pruebas para FileManager
def test_save_file_success():
    file_manager = FileManager()
    file_manager.save_file("valid_file.txt", "Este es un archivo válido.".encode("utf-8"))
    assert os.path.exists("./app/uploads/valid_file.txt")

def test_save_file_invalid_extension():
    file_manager = FileManager()
    with pytest.raises(ValueError):
        file_manager.save_file("invalid_file.pdf", "Contenido".encode("utf-8"))

def test_save_file_large_content():
    file_manager = FileManager()
    with pytest.raises(ValueError):
        file_manager.save_file("large_file.txt", ("A" * 1001).encode("utf-8"))

def test_delete_file_success():
    file_manager = FileManager()
    file_manager.save_file("valid_file.txt", "Contenido".encode("utf-8"))
    file_manager.delete_file("valid_file.txt")
    assert not os.path.exists("./app/uploads/valid_file.txt")

# Configuración del cliente Flask para pruebas
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(document_routes)
    client = app.test_client()
    yield client

# Pruebas para el endpoint /upload
def test_upload_success(client):
    """
    Subir un archivo válido debería ser exitoso.
    """
    data = {
        'file': (io.BytesIO("Contenido válido".encode("utf-8")), 'test_file.txt')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    response_json = response.get_json()
    assert response.status_code == 201
    assert response_json["message"] == "Archivo subido exitosamente."


def test_upload_no_file(client):
    """
    No enviar archivo debería devolver un error 400.
    """
    response = client.post('/upload')
    response_json = response.get_json()
    assert response.status_code == 400
    assert response_json["error"] == "No se encontró ningún archivo en la solicitud."


def test_upload_empty_file(client):
    """
    Enviar un archivo vacío debería devolver un error.
    """
    data = {
        'file': (io.BytesIO(b''), 'empty_file.txt')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    response_json = response.get_json()
    assert response.status_code == 400
    assert response_json["error"] == "El archivo no tiene contenido."


def test_upload_invalid_extension(client):
    """
    Subir un archivo con una extensión no permitida debería fallar.
    """
    data = {
        'file': (io.BytesIO("Contenido válido".encode("utf-8")), 'file.pdf')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    response_json = response.get_json()
    assert response.status_code == 400
    assert response_json["error"] == "Solo se permiten archivos con extensión .txt."


def test_upload_large_file(client):
    """
    Subir un archivo con más de 1000 caracteres debería fallar.
    """
    large_content = "A" * 1001
    data = {
        'file': (io.BytesIO(large_content.encode("utf-8")), 'large_file.txt')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    response_json = response.get_json()
    assert response.status_code == 400
    assert response_json["error"] == "El archivo supera el tamaño máximo permitido de 1000 caracteres."
