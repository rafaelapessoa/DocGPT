class HistoryManager:
    """
    Gestiona el registro de acciones realizadas en documentos y sesiones de chat.
    """

    def __init__(self):
        self.history = []

    def log_action(self, user_id: int, action_type: str, details: dict):
        """
        Registra una acción realizada por un usuario.
        """
        log_entry = {
            "user_id": user_id,
            "action_type": action_type,
            "details": details
        }
        self.history.append(log_entry)
        print(f"Acción registrada: {log_entry}")

    def retrieve_logs(self, user_id: int = None):
        """
        Recupera el historial de acciones.
        Si se proporciona un user_id, filtra por ese usuario.
        """
        if user_id:
            return [log for log in self.history if log["user_id"] == user_id]
        return self.history

    def delete_logs(self, user_id: int = None):
        """
        Elimina el historial de acciones. Si se proporciona un user_id, elimina solo las de ese usuario.
        """
        if user_id:
            self.history = [log for log in self.history if log["user_id"] != user_id]
            print(f"Historial eliminado para el usuario {user_id}.")
        else:
            self.history.clear()
            print("Todo el historial ha sido eliminado.")
