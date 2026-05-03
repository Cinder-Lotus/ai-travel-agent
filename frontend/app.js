// Generar un ID de sesión único y simple para esta ventana
const sessionId = 'session_' + Math.random().toString(36).substr(2, 9);
const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// URL de tu backend en FastAPI
const API_URL = 'http://localhost:8000/chat';

function addMessageToUI(role, text) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', role);
    
    const paragraph = document.createElement('p');
    // Para renderizar saltos de línea correctamente si Gemini usa Markdown básico
    paragraph.innerHTML = text.replace(/\n/g, '<br>'); 
    
    messageDiv.appendChild(paragraph);
    chatBox.appendChild(messageDiv);
    
    // Auto-scroll hacia abajo
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // Mostrar mensaje del usuario y limpiar input
    addMessageToUI('user', text);
    userInput.value = '';
    sendBtn.disabled = true;

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                message: text
            })
        });

        if (!response.ok) throw new Error("Error en el servidor");

        const data = await response.json();
        addMessageToUI('model', data.response);

    } catch (error) {
        console.error("Error:", error);
        addMessageToUI('model', 'Lo siento, hubo un error de conexión con mis sistemas. ¿Podemos intentarlo de nuevo?');
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// Event Listeners
sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});