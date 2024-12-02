import transformers
import torch
from huggingface_hub import login

# Autenticar con Hugging Face utilizando tu token
HF_API_TOKEN = "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"  # Sustituye con tu token real
login(token=HF_API_TOKEN)

# Identificador del modelo (modelo restringido)
model_id = "meta-llama/Meta-Llama-3-8B"

# Crear el pipeline
text_pipeline = transformers.pipeline(
    task="text-generation",
    model=model_id,
    device=0 if torch.cuda.is_available() else -1
)

# Usar el pipeline para generar texto
input_text = "Hey, how are you doing today?"
generated_text = text_pipeline(input_text, max_length=50, num_return_sequences=1)

# Mostrar la salida generada
print(generated_text)