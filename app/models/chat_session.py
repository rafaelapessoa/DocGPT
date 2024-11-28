class ChatSession:
    def __init__(self, session_id, user_id, document_id):
        self.session_id = session_id
        self.user_id = user_id
        self.document_id = document_id
        self.history = None
        self.active = False

    def start_session(self):
        if not self.active:
            self.history = []
            self.active = True
        print(f"Sesión de chat {self.session_id} iniciada.")

    def send_message(self, message):
        if not self.active:
            raise ValueError("No se puede enviar mensajes en una sesión no iniciada.")
        self.history.append({"user": message})
        print(f"Mensaje enviado: {message}")

    def get_history(self):
        if not self.active:
            raise ValueError("No se puede obtener el historial de una sesión no iniciada.")
        return self.history

    def end_session(self):
        if not self.active:
            raise ValueError("No se puede finalizar una sesión no iniciada.")
        self.active = False
        print(f"Sesión de chat {self.session_id} finalizada.")
