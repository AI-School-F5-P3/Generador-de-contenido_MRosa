from fastapi import FastAPI, HTTPException
from src.moderation import Moderation
from src.prompt_manager import PromptManager, PROMPTS
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
async def generar_contenido(request: PromptManager):
    # Moderar el texto
    texto_completo = f"{request.topic} {request.audience}"
    score = moderation.validar_moderacion(texto_completo)
    if score > 0.5:
        raise HTTPException(
            status_code=400,
            detail=f"Por favor, revisa el texto para evitar lenguaje ofensivo antes de enviarlo (score={score:.2f})."
        )

    # Validar la plataforma
    if request.platform not in PROMPTS:
        raise HTTPException(status_code=400, detail="Plataforma no soportada.")

    # Crear el prompt utilizando el método generate_prompt
    try:
        prompt = request.generate_prompt()  # Personalización incluida en generate_prompt
        print("\n============================= prompt =========================================\n")
        print(prompt)
        print("\n================================================================================\n")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # prompt = prompt[:1500]


    try:
        respuesta = model_client.generar_respuesta(prompt, max_tokens=1500, temperature=0.3, top_p=0.9)
        return {"respuesta": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
