# DocGPT: Micro Corpus con Inteligencia Artificial

DocGPT es una herramienta diseñada para integrar capacidades de inteligencia artificial en documentos privados. Permite realizar tareas como traducciones, resúmenes y modificaciones en los textos subidos, garantizando privacidad y seguridad. Esta aplicación es ideal para manejar información sensible de manera eficiente.

---

## **Características Principales**
- **Interfaz de chat**: Interactúa en tiempo real con la IA.
- **Historial de documentos**: Rastrear cambios y conversaciones.
- **Carga de archivos**: Sube y gestiona documentos de manera segura.
- **Backend impulsado por IA**: Conexión directa con Ollama para procesar entradas.
- **Acciones disponibles**:
  - **Summarize**: Genera resúmenes de documentos.
  - **Translate**: Traduce documentos a otros idiomas.
  - **Modify**: Realiza modificaciones en el contenido según instrucciones específicas.

---

## **Requisitos**
1. **Software**:
   - Python 3.10 o superior.
   - Postman (para pruebas de API).
   - Ollama instalado y configurado correctamente.

2. **Modelos de Ollama**:
   - Modelos compatibles (e.g., `llama3.2` o `llama2`).
   - Asegúrate de que el servidor de Ollama esté funcionando:
     ```bash
     ollama serve
     ```

---

## **Instalación**

### 1. Clona el Repositorio
```bash
git clone https://github.com/tu-usuario/docgpt.git
cd docgpt
