import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# 1. Configurar la API Key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Instrucciones del sistema
sys_instruct = """
Eres un agente de viajes IA ultraconciso y proactivo. 

Reglas estrictas de operación:
1. ORIGEN FIJO: Todos los vuelos de salida son SIEMPRE desde el Aeropuerto Alfonso Bonilla Aragón (CLO) en Cali, Colombia. No preguntes desde dónde viaja el usuario.
2. AUTONOMÍA: El usuario solo te indicará el destino (y quizás los días). No hagas preguntas de seguimiento ni pidas presupuestos. Genera el itinerario completo por tu cuenta de forma lógica.
3. Explicacion detallada: Entra en detalle en lo que se va a ser en cada dia , ademas de decir el precio estimado de todo el viaje en pesos colombianos
4. ENLACES DE RESERVA: Al final de tu respuesta, debes incluir enlaces reales a plataformas de reserva. Usa el destino solicitado por el usuario para armar enlaces de búsqueda genéricos pero útiles.

Formato de salida esperado:
- 🛫 **Vuelos:** 
- 🏨 **Alojamiento:** 
- 📅 **Itinerario [X] Días:**
  - Día 1: [Actividad principal]
  - Día 2: [Actividad principal]

Lo que son vuelos, alojamientos e itinerarios, deben ser reales y específicos para el destino solicitado por el usuario. No inventes información ni enlaces. Si no puedes encontrar algo específico, omítelo pero no dejes campos vacíos.  
"""

# 3. Inicializar el modelo con las instrucciones
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=sys_instruct,
    generation_config={"temperature": 0.7}
)

def get_travel_response(user_message: str, chat_history: list) -> str:
    # 4. Formatear el historial recuperado de Astra DB para Gemini
    formatted_history = []
    for msg in chat_history:
        # Asegurar que los roles sean exactamente "user" o "model"
        role = "user" if msg["role"] == "user" else "model"
        formatted_history.append({
            "role": role,
            "parts": [msg["content"]]
        })
    
    # 5. Crear la sesión de chat inyectando el historial anterior
    chat = model.start_chat(history=formatted_history)
    
    # 6. Enviar el mensaje actual a Gemini y retornar la respuesta
    response = chat.send_message(user_message)
    return response.text