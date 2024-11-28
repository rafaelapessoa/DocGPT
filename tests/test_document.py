import pytest
from flask import Flask
from app.models.document import Document
from app.routes.document_routes import document_routes, documents_db

# Pruebas unitarias para la clase Document
def test_upload_document_success():
    doc = Document(1, 1, "example.txt", "Contenido inicial", {"author": "test_user"})
    doc.upload("Nuevo contenido")
    assert doc.content == "Nuevo contenido"

def test_update_content_success():
    doc = Document(1, 1, "example.txt", "Contenido inicial", {"author": "test_user"})
    doc.update_content("Contenido actualizado")
    assert doc.content == "Contenido actualizado"

def test_get_metadata_success():
    metadata = {"author": "test_user"}
    doc = Document(1, 1, "example.txt", "Contenido inicial", metadata)
    assert doc.get_metadata() == metadata

# Pruebas para los endpoints /documents y /document/<id>
@pytest.fixture
def client():
    """
    Configura el cliente Flask para las pruebas.
    """
    app = Flask(__name__)
    app.register_blueprint(document_routes)
    client = app.test_client()
    yield client

def test_list_documents_empty(client):
    """
    Obtener la lista de documentos debería devolver vacío si no hay documentos.
    """
    response = client.get('/documents')
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json["documents"] == []

def test_list_documents_with_data(client):
    """
    Obtener la lista de documentos debería devolver datos si existen documentos.
    """
    # Simula un documento en la base de datos
    documents_db[1] = Document(1, 1, "test_file.txt", "Contenido", {"author": "test_user"})

    response = client.get('/documents')
    response_json = response.get_json()
    assert response.status_code == 200
    assert len(response_json["documents"]) == 1
    assert response_json["documents"][0]["filename"] == "test_file.txt"

def test_get_document_success(client):
    """
    Obtener un documento existente debería devolver su contenido.
    """
    # Simula un documento en la base de datos
    documents_db[1] = Document(1, 1, "test_file.txt", "Contenido", {"author": "test_user"})

    response = client.get('/document/1')
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json["filename"] == "test_file.txt"
    assert response_json["content"] == "Contenido"
    assert response_json["metadata"]["author"] == "test_user"

def test_get_document_not_found(client):
    """
    Intentar obtener un documento inexistente debería devolver un error 404.
    """
    response = client.get('/document/999')
    response_json = response.get_json()
    assert response.status_code == 404
    assert response_json["error"] == "Documento no encontrado."
