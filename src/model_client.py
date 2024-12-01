# from huggingface_hub import InferenceClient

# class ModelClient:
#     def __init__(self, model_name: str, hf_token: str):
#         self.client = InferenceClient(model=model_name, token=hf_token)

#     def generar_respuesta(self, prompt: str, max_tokens: int = 1500):
#         messages = [{"role": "user", "content": prompt}]

#         response = self.client.chat_completion(messages=messages, max_tokens=max_tokens)
#         response = client.generar_respuesta(
#             prompt,
#             max_tokens=200,
#             temperature=0.3,  # Menos aleatoriedad, ideal para código
#             top_p=0.9         # Control de probabilidad acumulada
#         )

#         if hasattr(response, "choices") and response.choices:
#             return response.choices[0].message["content"]
#         else:
#             raise ValueError("No se recibió una respuesta válida del modelo.")

from huggingface_hub import InferenceClient

class ModelClient:
    def __init__(self, model_name: str, hf_token: str):
        """
        Inicializa el cliente para interactuar con el modelo en Hugging Face.
        
        Args:
        - model_name (str): Nombre del modelo a utilizar.
        - hf_token (str): Token de acceso de Hugging Face.
        """
        self.client = InferenceClient(model=model_name, token=hf_token)

    def generar_respuesta(self, prompt: str, max_tokens: int = 1500, temperature: float = 0.3, top_p: float = 0.9):
        """
        Genera una respuesta basada en el prompt proporcionado.
        
        Args:
        - prompt (str): Entrada para el modelo.
        - max_tokens (int): Número máximo de tokens en la respuesta generada.
        - temperature (float): Controla la aleatoriedad en las respuestas (0.0 a 1.0).
        - top_p (float): Filtrado de tokens por probabilidad acumulada (0.0 a 1.0).

        Returns:
        - str: Respuesta generada por el modelo.
        """
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p
        )
        if hasattr(response, "choices") and response.choices:
            return response.choices[0].message["content"]
        else:
            raise ValueError("No se recibió una respuesta válida del modelo.")
