import os

class FileManager:
    """
    Gestiona la carga, almacenamiento y eliminación de archivos.
    """

    def __init__(self, storage_path: str = "./app/uploads", max_size: int = 1000, allowed_types: list = None):
        """
        Inicializa el administrador de archivos.
        - storage_path: Ruta donde se almacenan los archivos.
        - max_size: Tamaño máximo permitido en caracteres.
        - allowed_types: Lista de extensiones de archivo permitidas.
        """
        self.storage_path = storage_path
        self.max_size = max_size
        self.allowed_types = allowed_types if allowed_types else ["txt"]

        # Crear la carpeta de almacenamiento si no existe
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def save_file(self, file_name: str, file_content: bytes):
        """
        Guarda un archivo en el sistema.
        - file_name: Nombre del archivo (incluye la extensión).
        - file_content: Contenido del archivo en bytes.
        """
        # Validar extensión
        if not file_name.split(".")[-1] in self.allowed_types:
            raise ValueError("Tipo de archivo no permitido. Solo se admiten archivos .txt.")
        
        # Validar tamaño en caracteres
        try:
            # Decodificar contenido a UTF-8 para contar caracteres
            content_length = len(file_content.decode("utf-8"))
        except UnicodeDecodeError:
            raise ValueError("El contenido del archivo no es válido. Asegúrate de que sea texto.")

        if content_length > self.max_size:
            raise ValueError(f"El archivo excede el tamaño máximo permitido de {self.max_size} caracteres.")
        
        # Guardar archivo
        file_path = os.path.join(self.storage_path, file_name)
        with open(file_path, "wb") as f:
            f.write(file_content)
        print(f"Archivo {file_name} guardado en {self.storage_path}.")

    def delete_file(self, file_name: str):
        """
        Elimina un archivo del sistema.
        - file_name: Nombre del archivo a eliminar.
        """
        file_path = os.path.join(self.storage_path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Archivo {file_name} eliminado.")
        else:
            raise FileNotFoundError("El archivo no existe.")
