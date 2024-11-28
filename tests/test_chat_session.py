import pytest
from app.models.chat_session import ChatSession

# Pruebas para iniciar una sesión de chat
def test_start_chat_session_success():
    """
    Iniciar una sesión de chat debería ser exitoso.
    """
    chat = ChatSession(1, 1, 1)
    chat.start_session()
    assert chat.history == []

def test_start_chat_session_already_started():
    """
    Intentar iniciar una sesión ya iniciada debería mantener el historial vacío.
    """
    chat = ChatSession(1, 1, 1)
    chat.start_session()
    chat.start_session()  # Repetir inicio de sesión
    assert chat.history == []

# Pruebas para enviar mensajes
def test_send_message_success():
    """
    Enviar un mensaje debería agregarlo al historial de la sesión.
    """
    chat = ChatSession(1, 1, 1)
    chat.start_session()
    chat.send_message("Hola, IA!")
    assert chat.history == [{"user": "Hola, IA!"}]

def test_send_message_without_starting():
    """
    Enviar un mensaje sin iniciar la sesión debería lanzar un ValueError.
    """
    chat = ChatSession(1, 1, 1)
    with pytest.raises(ValueError):
        chat.send_message("Hola, IA!")

# Pruebas para obtener historial
def test_get_history_success():
    """
    Obtener el historial de una sesión debería devolver los mensajes enviados.
    """
    chat = ChatSession(1, 1, 1)
    chat.start_session()
    chat.send_message("Hola, IA!")
    history = chat.get_history()
    assert history == [{"user": "Hola, IA!"}]

def test_get_history_empty():
    """
    Obtener el historial de una sesión sin mensajes debería devolver una lista vacía.
    """
    chat = ChatSession(1, 1, 1)
    chat.start_session()
    assert chat.get_history() == []

# Pruebas para finalizar la sesión
def test_end_chat_session_success():
    """
    Finalizar una sesión debería mantener el historial accesible como una lista.
    """
    chat = ChatSession(1, 1, 1)
    chat.start_session()
    chat.end_session()
    assert isinstance(chat.history, list)

def test_end_chat_session_without_starting():
    """
    Finalizar una sesión sin iniciarla debería lanzar un ValueError.
    """
    chat = ChatSession(1, 1, 1)
    with pytest.raises(ValueError):
        chat.end_session()
