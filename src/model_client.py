from huggingface_hub import InferenceClient

class ModelClient:
    def __init__(self, model_name: str, hf_token: str):
        self.client = InferenceClient(model=model_name, token=hf_token)

    def generar_respuesta(self, prompt: str, max_tokens: int = 1500):
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat_completion(messages=messages, max_tokens=max_tokens)
        if hasattr(response, "choices") and response.choices:
            return response.choices[0].message["content"]
        else:
            raise ValueError("No se recibió una respuesta válida del modelo.")
