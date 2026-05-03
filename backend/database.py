import os
from dotenv import load_dotenv
from astrapy import DataAPIClient

load_dotenv()

ASTRA_DB_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")

# Inicializar cliente y base de datos
client = DataAPIClient(ASTRA_DB_TOKEN)
db = client.get_database_by_api_endpoint(ASTRA_DB_ENDPOINT)

# Seleccionar la colección (equivalente a una tabla). 
# Si no existe en la BD, puedes crearla descomentando la siguiente línea la primera vez que ejecutes:
db.create_collection("chat_history")
history_collection = db.get_collection("chat_history")

def save_message(session_id: str, role: str, content: str):
    """Guarda un mensaje en la base de datos."""
    history_collection.insert_one({
        "session_id": session_id,
        "role": role,
        "content": content
    })

def get_history(session_id: str) -> list:
    """Recupera el historial ordenado (asumiendo que Astra devuelve el orden de inserción)."""
    results = history_collection.find({"session_id": session_id})
    return list(results)