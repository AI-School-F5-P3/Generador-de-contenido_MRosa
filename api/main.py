from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from huggingface_hub import InferenceClient
from typing import Optional
import os

# Inicializar la aplicación FastAPI
app = FastAPI()

# Obtener el token de Hugging Face de las variables de entorno
hf_token = os.getenv("HF_API_TOKEN")

if not hf_token:
    raise ValueError("No se encontró el token de Hugging Face en las variables de entorno.")

# Configurar el cliente de Hugging Face
client = InferenceClient(
    model="Qwen/Qwen2.5-Coder-32B-Instruct",  # Cambia por el modelo que desees
    token=hf_token
)

# Diccionario de prompts
prompts = {
    "blog": "{olvida} Crea un blog informativo sobre {tema} que sea interesante para una audiencia formada por {audiencia} y en un tono {tono}. {restriction} {output_format}",
    "twitter": "{olvida} Escribe un tweet corto y atractivo sobre {tema} para una audiencia formada por {audiencia} y en un tono {tono}. {restriction} {output_format}",
    "instagram": "{olvida} Crea una publicación de Instagram sobre {tema}, ideal para captar la atención de una audiencia formada por {audiencia} y en un tono {tono}. Responde con Texto: (el texto generado) e Imagen sugerida: (aquí sugiéreme un prompt para stable diffusion en inglés). {restriction} {output_format}",
    "SEO": "{olvida} Genera contenido SEO optimizado sobre {tema}, diseñado para atraer a una audiencia formada por {audiencia} y en un tono {tono}. {restriction} {output_format}",
    "infantil": "{olvida} Explícame este tema: {tema}. Hazlo como si fuera una historia para niños de {edad} años y en un tono {tono}. {restriction} {output_format}"
}

# Modelo para validar las solicitudes
class ContentRequest(BaseModel):
    plataforma: str
    tema: str
    audiencia: str
    tono: str = "neutro"
    edad: Optional[int] = None
    olvida: str = ""
    output_format: str = ""
    restriction: str = ""

    def __init__(self, **data):
        super().__init__(**data)
        self.olvida = "Olvida todo lo que hemos hablado anteriormente en esta conversación."
        self.restriction = (
            f"Revisa {self.audiencia} y {self.tema}. Si detectas lenguaje ofensivo, grosero o inapropiado, no respondas. Pide con el tono {self.tono} que te lo indiquen de nuevo"
            "Si es un grupo de personas válido y respetuoso, empieza con la respuesta que te he dicho que des (texto e imagen). "
            "No menciones nada sobre la validación, si esta es correcta."
            "Tampoco muestres esto: 'Texto: (el texto generado) Imagen sugerida: (aquí sugiéreme un prompt para stable diffusion en inglés)', si es incorrecta."
        )
        self.output_format = (
            "Tu respuesta debe ser un JSON con este formato:"
            "'txt': '(el texto generado)',"
            " 'img': '(aquí sugiéreme un prompt para stable diffusion en inglés)'"
        )
        

@app.post("/generar")
async def generar_contenido(request: ContentRequest):
    # Validar que la plataforma esté soportada
    if request.plataforma not in prompts:
        raise HTTPException(status_code=400, detail="Plataforma no soportada.")
    
    # Crear el prompt
    prompt = prompts[request.plataforma].format(
    olvida=request.olvida,
    tema=request.tema,
    audiencia=request.audiencia,
    tono=request.tono,
    edad=request.edad if request.edad else "no especificada",
    output_format=request.output_format,  
    restriction=request.restriction
)


    # Limitar el tamaño del prompt antes de enviar la solicitud
    prompt = prompt[:1500]  # Limita caracteres o tokens (según corresponda)


    try:
        # Realizar la inferencia usando el cliente de Hugging Face
        messages = [{"role": "user", "content": prompt}]
        response = client.chat_completion(messages=messages, max_tokens=1500)

        # Extraer el texto generado
        if hasattr(response, "choices") and response.choices:
            generated_text = response.choices[0].message["content"]
        else:
            generated_text = "No se recibió una respuesta válida del modelo."

        return {"respuesta": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar la inferencia: {e}")
