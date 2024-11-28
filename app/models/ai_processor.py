import subprocess
import json

class AIProcessor:
    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name

    def _call_ollama(self, prompt):
        """
        Llama a Ollama con un prompt y devuelve la respuesta.
        """
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name],
                input=json.dumps({"prompt": prompt}),
                text=True,
                capture_output=True,
                check=True
            )
            # Imprimir la salida para depuración
            print("Salida de Ollama (stdout):", result.stdout)
            print("Error de Ollama (stderr):", result.stderr)

            # Intentar parsear la respuesta como JSON
            try:
                response = json.loads(result.stdout)
                return response.get("response", result.stdout.strip())
            except json.JSONDecodeError:
                # Si el JSON no es válido, devolvemos el texto crudo
                print("Respuesta en texto plano:", result.stdout.strip())
                return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error llamando a Ollama: {e.stderr}")

    def summarize(self, content):
        if not content:
            raise ValueError("El contenido no puede estar vacío.")
        prompt = f"Resume el siguiente texto:\n\n{content}"
        return self._call_ollama(prompt)

    def translate(self, content, target_language):
        if not target_language:
            raise ValueError("El idioma destino no puede estar vacío.")
        if not content:
            raise ValueError("El contenido no puede estar vacío.")
        prompt = f"Traduce el siguiente texto al {target_language}:\n\n{content}"
        return self._call_ollama(prompt)

    def modify_content(self, content, instructions):
        if not instructions:
            raise ValueError("Las instrucciones no pueden estar vacías.")
        if not content:
            raise ValueError("El contenido no puede estar vacío.")
        prompt = f"Modifica el siguiente texto basado en estas instrucciones:\n\n{instructions}\n\nTexto:\n\n{content}"
        return self._call_ollama(prompt)