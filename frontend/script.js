const baseURL = "http://127.0.0.1:5000";

// Subir Documento
document.querySelector("button[type='submit']").addEventListener("click", async (e) => {
    e.preventDefault(); // Prevenir recarga
    console.log("Botón de subir archivo clicado.");

    const fileInput = document.getElementById("file-input");
    const uploadResult = document.getElementById("upload-result");

    // Limpiar mensajes previos
    uploadResult.innerText = "";

    // Validar si hay un archivo seleccionado
    if (!fileInput.files.length) {
        console.error("No se ha seleccionado ningún archivo.");
        uploadResult.innerText = "Por favor, selecciona un archivo antes de subirlo.";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch(`${baseURL}/upload`, {
            method: "POST",
            body: formData,
        });

        // Verificar si la respuesta es válida
        if (!response.ok) {
            const errorData = await response.json();
            console.error("Error al subir el archivo:", errorData.error);
            uploadResult.innerText = `Error: ${errorData.error}`;
            return;
        }

        const data = await response.json();
        console.log("Archivo subido con éxito:", data);
        uploadResult.innerText = `Archivo subido con éxito: Document ID: ${data.document_id}`;
    } catch (error) {
        console.error("Error en la solicitud:", error);
        uploadResult.innerText = "Error al subir el archivo. Por favor, intenta nuevamente.";
    }
});

// Listar Documentos
document.getElementById("list-documents").addEventListener("click", async () => {
    try {
        const response = await fetch(`${baseURL}/documents`);
        const data = await response.json();
        const list = document.getElementById("documents-list");
        list.innerHTML = ""; // Limpiar la lista
        data.documents.forEach((doc) => {
            const li = document.createElement("li");
            li.innerText = `ID: ${doc.document_id}, Nombre: ${doc.filename}`;
            list.appendChild(li);
        });
    } catch (error) {
        document.getElementById("documents-list").innerText = "Error al listar documentos.";
    }
});

// Procesar Documento
document.getElementById("process-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const documentId = document.getElementById("document-id").value;
    const action = document.getElementById("action").value;
    const extraInput = document.getElementById("extra-input").value;

    const body = {
        document_id: parseInt(documentId),
        action,
    };

    if (action === "translate") {
        body.target_language = extraInput;
    } else if (action === "modify") {
        body.instructions = extraInput;
    }

    try {
        const response = await fetch(`${baseURL}/process`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });
        const data = await response.json();
        document.getElementById("process-result").innerHTML = data.result
        .replace(/\n{2,}/g, "<br><br>") // Reemplazar múltiples saltos de línea con dos <br>
        .replace(/\n/g, "<br>")         // Reemplazar un único salto de línea con <br>
        .replace(/\\/g, "");            // Eliminar barras invertidas
    } catch (error) {
        document.getElementById("process-result").innerText = "Error al procesar el documento.";
    }
});

let currentSessionId = null;

// Enviar Mensaje
document.getElementById("send-message-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const message = document.getElementById("message-input").value;

    try {
        const response = await fetch(`${baseURL}/chat/send`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();

        if (response.ok) {
            const chatHistory = document.getElementById("chat-history");

            // Agregar mensaje del usuario
            const userMessage = document.createElement("li");
            userMessage.className = "user";
            userMessage.innerText = `Usuario: ${message}`;
            chatHistory.appendChild(userMessage);

            // Agregar respuesta del bot
            const botMessage = document.createElement("li");
            botMessage.className = "bot";
            botMessage.innerText = `Bot: ${data.chat_history[data.chat_history.length - 1]?.bot || "Sin respuesta del bot."}`;
            chatHistory.appendChild(botMessage);

            // Limpiar el input del mensaje
            document.getElementById("message-input").value = "";
        } else {
            alert(data.error || "Error al enviar el mensaje.");
        }
    } catch (error) {
        console.error("Error en la solicitud:", error);
        alert("Error al enviar el mensaje.");
    }
});




