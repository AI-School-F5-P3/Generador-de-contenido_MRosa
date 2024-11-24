from fastapi import FastAPI, HTTPException
from src.moderation import Moderation
from src.prompt_manager import ContentRequest, PROMPTS
from src.model_client import ModelClient
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))


# Inicializar FastAPI
app = FastAPI()

# Inicializar modelos y cliente
moderation = Moderation()
hf_token = os.getenv("HF_API_TOKEN")
if not hf_token:
    raise ValueError("No se encontró el token de Hugging Face en las variables de entorno.")
model_client = ModelClient(model_name="Qwen/Qwen2.5-Coder-32B-Instruct", hf_token=hf_token)

@app.post("/generar")
async def generar_contenido(request: ContentRequest):
    # Moderar el texto
    texto_completo = f"{request.tema} {request.audiencia}"
    score = moderation.validar_moderacion(texto_completo)
    if score > 0.5:
        raise HTTPException(
            status_code=400, 
            detail=f"El texto contiene contenido potencialmente ofensivo (score={score:.2f})."
        )

    # Validar la plataforma
    if request.plataforma not in PROMPTS:
        raise HTTPException(status_code=400, detail="Plataforma no soportada.")
    
    # Crear el prompt
    prompt = PROMPTS[request.plataforma].format(
        idioma=request.idioma,
        olvida=request.olvida,
        tema=request.tema,
        audiencia=request.audiencia,
        tono=request.tono,
        edad=request.edad if request.edad else "no especificada",
        output_format=request.output_format,  
        restriction=request.restriction
    )

    # Limitar el tamaño del prompt
    prompt = prompt[:1500]

    try:
        respuesta = model_client.generar_respuesta(prompt)
        return {"respuesta": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
