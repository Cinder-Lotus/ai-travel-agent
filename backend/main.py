from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_history, save_message
from ai_agent import get_travel_response

app = FastAPI()

# Configurar CORS para permitir peticiones desde el frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción, cambia "*" por la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # 1. Recuperar historial de Astra DB
    history = get_history(request.session_id)
    
    # 2. Guardar el nuevo mensaje del usuario
    save_message(request.session_id, "user", request.message)
    
    # 3. Consultar a Gemini
    ai_response = get_travel_response(request.message, history)
    
    # 4. Guardar la respuesta del modelo
    save_message(request.session_id, "model", ai_response)
    
    return {"response": ai_response}

# Para ejecutar el servidor usa: uvicorn main:app --reload