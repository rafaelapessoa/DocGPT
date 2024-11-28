class Document:
    """
    Representa un documento subido por el usuario.
    """

    def __init__(self, id: int, user_id: int, filename: str, content: str, metadata: dict):
        self.id = id
        self.user_id = user_id
        self.filename = filename
        self.content = content
        self.metadata = metadata

    def upload(self, content: str):
        """
        Subir contenido al documento.
        """
        self.content = content
        print(f"Contenido subido al documento {self.filename}.")

    def delete(self):
        """
        Eliminar el documento.
        """
        # Implementar lógica para eliminar documento
        print(f"Documento {self.filename} eliminado.")

    def get_metadata(self):
        """
        Obtener metadatos del documento.
        """
        return self.metadata

    def update_content(self, new_content: str):
        """
        Actualiza el contenido del documento.
        """
        self.content = new_content
        print(f"Contenido del documento {self.filename} actualizado.")
