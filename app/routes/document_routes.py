from flask import Blueprint, request, jsonify
from app.models.file_manager import FileManager
from app.models.document import Document
from app.models.chat_session import ChatSession
from app.models.ai_processor import AIProcessor

# RUTAS RESTFUL PARA LOS DOCUMENTOS Y CHAT.

# Crear un Blueprint para las rutas de documentos
document_routes = Blueprint('document_routes', __name__)

# Simulador de base de datos en memoria para documentos y sesiones de chat
documents_db = {}
chat_sessions_db = {}

# Instancia de FileManager y AIProcessor
file_manager = FileManager()
ai_processor = AIProcessor(model_name="llama3.2")


@document_routes.route('/upload', methods=['POST'])
def upload_document():
    """
    Sube un documento al servidor y lo guarda en la base de datos simulada.
    """
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({"error": "No se encontró ningún archivo en la solicitud."}), 400

    file = request.files['file']
    file_name = file.filename
    file_content = file.read()

    # Validaciones adicionales
    if len(file_content) == 0:
        return jsonify({"error": "El archivo no tiene contenido."}), 400

    if not file_name.endswith('.txt'):
        return jsonify({"error": "Solo se permiten archivos con extensión .txt."}), 400

    if len(file_content.decode('utf-8')) > 1000:
        return jsonify({"error": "El archivo supera el tamaño máximo permitido de 1000 caracteres."}), 400

    # Guardar el archivo usando FileManager
    file_manager.save_file(file_name, file_content)

    # Crear un documento en la base de datos simulada
    doc_id = len(documents_db) + 1
    new_document = Document(doc_id, 1, file_name, file_content.decode('utf-8'), {"author": "anonymous"})
    documents_db[doc_id] = new_document

    return jsonify({"message": "Archivo subido exitosamente.", "document_id": doc_id}), 201


@document_routes.route('/document/<int:doc_id>', methods=['GET'])
def get_document(doc_id):
    """
    Recupera un documento por su ID desde la base de datos simulada.
    """
    document = documents_db.get(doc_id)
    if not document:
        return jsonify({"error": "Documento no encontrado."}), 404

    return jsonify({
        "document_id": document.id,
        "filename": document.filename,
        "content": document.content,
        "metadata": document.metadata
    }), 200


@document_routes.route('/documents', methods=['GET'])
def list_documents():
    """
    Lista todos los documentos en la base de datos simulada.
    """
    documents = [
        {
            "document_id": doc.id,
            "filename": doc.filename,
            "content": doc.content,
            "metadata": doc.metadata
        }
        for doc in documents_db.values()
    ]

    return jsonify({"documents": documents}), 200


@document_routes.route('/process', methods=['POST'])
def process_document():
    """
    Procesa un documento basado en la acción especificada utilizando Ollama.
    """
    data = request.get_json()

    # Validar que los parámetros necesarios están presentes
    if not data or 'document_id' not in data or 'action' not in data:
        return jsonify({"error": "Se requieren 'document_id' y 'action'."}), 400

    document_id = data['document_id']
    action = data['action']
    instructions = data.get('instructions', '')  # Opcional

    # Buscar el documento en la base de datos simulada
    document = documents_db.get(document_id)
    if not document:
        return jsonify({"error": "Documento no encontrado."}), 404

    try:
        # Procesar con AIProcessor
        ai_processor = AIProcessor()
        if action == 'summarize':
            result = ai_processor.summarize(document.content)
        elif action == 'translate':
            if 'target_language' not in data:
                return jsonify({"error": "Se requiere 'target_language' para traducir."}), 400
            result = ai_processor.translate(document.content, data['target_language'])
        elif action == 'modify':
            if not instructions:
                return jsonify({"error": "Se requieren 'instructions' para modificar."}), 400
            result = ai_processor.modify_content(document.content, instructions)
        else:
            return jsonify({"error": "Acción no soportada."}), 400

        # Responder con el resultado
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@document_routes.route('/chat/send', methods=['POST'])
def send_message_to_chat():
    """
    Envía un mensaje al chat y obtiene una respuesta de Ollama.
    El chat no requiere iniciar sesiones explícitas; simplemente responde al mensaje enviado.
    """
    data = request.get_json()

    # Validar que se envíe un mensaje
    if not data or 'message' not in data:
        return jsonify({"error": "Se requiere 'message' para enviar un mensaje."}), 400

    message = data['message']

    # Crear un historial local temporal para mantener el contexto (si es necesario)
    chat_history = [{"user": message}]

    # Llamar a Ollama para generar la respuesta
    try:
        ai_processor = AIProcessor()
        response = ai_processor.modify_content(message, "Responde como un asistente de IA.")

        # Si la respuesta está vacía o no válida, manejarla
        if not response.strip():
            response = "Lo siento, no tengo una respuesta para eso."

        # Agregar la respuesta al historial
        chat_history.append({"bot": response})

        return jsonify({
            "message": "Mensaje enviado con éxito.",
            "chat_history": chat_history  # Devolver el historial actualizado
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error al procesar el mensaje: {str(e)}"}), 500


