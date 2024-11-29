from app.models.document import Document
from app.models.chat_session import ChatSession
from app.models.ai_processor import AIProcessor
from app.models.file_manager import FileManager
from app.models.history_manager import HistoryManager
from app import create_app
from flask_cors import CORS
import os

# Configuración de encoding
os.environ["PYTHONIOENCODING"] = "utf-8"

# Crear la app de Flask
app = create_app()

# Habilitar CORS para toda la app y permitir solicitudes desde el frontend
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})


# Punto de entrada principal
if __name__ == "__main__":
    app.run(debug=True)


# Prueba rápida de Document
doc = Document(1, 1, "example.txt", "Contenido inicial", {"author": "test_user"})
doc.upload("Nuevo contenido")
print(doc.get_metadata())

# Prueba rápida de ChatSession
chat = ChatSession(1, 1, 1)
chat.start_session()
chat.send_message("Hola, IA!")
print(chat.get_history())
chat.end_session()

# Prueba rápida de AIProcessor
ai_processor = AIProcessor(api_key="test_key", model_name="test_model")
print(ai_processor.summarize("Este es un texto de prueba."))

# Prueba rápida de FileManager
file_manager = FileManager(storage_path="./app/uploads")

# Caso exitoso: Archivo válido
try:
    file_manager.save_file("valid_file.txt", "Este es un archivo válido con menos de 1000 caracteres.".encode("utf-8"))
    print("Archivo guardado correctamente.")
except ValueError as e:
    print(f"Error: {e}")

# Caso de error: Archivo con extensión no permitida
try:
    file_manager.save_file("invalid_file.pdf", "Contenido inválido.".encode("utf-8"))
except ValueError as e:
    print(f"Error: {e}")

# Caso de error: Archivo con más de 1000 caracteres
try:
    file_manager.save_file("large_file.txt", ("A" * 1001).encode("utf-8"))
except ValueError as e:
    print(f"Error: {e}")

# Eliminar un archivo válido
try:
    file_manager.delete_file("valid_file.txt")
    print("Archivo eliminado correctamente.")
except FileNotFoundError as e:
    print(f"Error: {e}")

# Prueba rápida de HistoryManager
history_manager = HistoryManager()
history_manager.log_action(1, "upload", {"filename": "example.txt"})
print(history_manager.retrieve_logs())
history_manager.delete_logs(1)
