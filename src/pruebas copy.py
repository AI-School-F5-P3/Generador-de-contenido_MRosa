# import torch
# from diffusers import FluxPipeline

# class GeneradorImagenesFlux:
#     def __init__(self, modelo: str = "black-forest-labs/FLUX.1-dev", dispositivo: str = "cuda"):
#         """
#         Inicializa el generador de imágenes utilizando el modelo FLUX.

#         :param modelo: Nombre del modelo preentrenado en Hugging Face.
#         :param dispositivo: Dispositivo para la ejecución ('cuda' o 'cpu').
#         """
#         self.dispositivo = dispositivo
#         self.pipeline = FluxPipeline.from_pretrained(modelo, torch_dtype=torch.bfloat16)
#         if dispositivo == "cuda":
#             self.pipeline.to(dispositivo)
#         self.pipeline.enable_model_cpu_offload()  # Offload para ahorrar memoria VRAM en GPU.

#     def generar_imagen(self, texto: str, archivo_salida: str = "imagen_flux.png", alto: int = 1024, ancho: int = 1024,
#                        guidance_scale: float = 3.5, num_steps: int = 50, semilla: int = 0):
#         """
#         Genera una imagen a partir de un texto utilizando FLUX.

#         :param texto: Texto para generar la imagen.
#         :param archivo_salida: Ruta del archivo donde se guardará la imagen generada.
#         :param alto: Altura de la imagen generada.
#         :param ancho: Ancho de la imagen generada.
#         :param guidance_scale: Escala de orientación para controlar la calidad de la generación.
#         :param num_steps: Número de pasos de inferencia para la generación.
#         :param semilla: Semilla para reproducibilidad en la generación.
#         """
#         try:
#             # Configuración del generador para reproducibilidad
#             generador = torch.Generator("cpu").manual_seed(semilla)

#             # Generar la imagen
#             imagen = self.pipeline(
#                 texto,
#                 height=alto,
#                 width=ancho,
#                 guidance_scale=guidance_scale,
#                 num_inference_steps=num_steps,
#                 max_sequence_length=512,
#                 generator=generador
#             ).images[0]

#             # Guardar la imagen generada
#             imagen.save(archivo_salida)
#             print(f"Imagen generada y guardada como {archivo_salida}.")
#             return archivo_salida
#         except Exception as e:
#             print(f"Error al generar la imagen: {e}")
#             return None

# # Ejemplo de uso
# if __name__ == "__main__":
#     generador = GeneradorImagenesFlux()
#     texto = "Un gato sosteniendo un cartel que dice hola mundo"
#     generador.generar_imagen(
#         texto,
#         archivo_salida="gato_flux.png",
#         alto=1024,
#         ancho=1024,
#         guidance_scale=3.5,
#         num_steps=50,
#         semilla=42
#     )
##################################################################################
# import torch
# from diffusers import StableCascadeCombinedPipeline

# pipe = StableCascadeCombinedPipeline.from_pretrained("stabilityai/stable-cascade", variant="bf16", torch_dtype=torch.bfloat16)

# prompt = "an image of a shiba inu, donning a spacesuit and helmet"
# pipe(
#     prompt=prompt,
#     negative_prompt="",
#     num_inference_steps=10,
#     prior_num_inference_steps=20,
#     prior_guidance_scale=3.0,
#     width=1024,
#     height=1024,
# ).images[0].save("cascade-combined.png")
###################################################################################
# import urllib, urllib.request

# url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'
# data = urllib.request.urlopen(url)
# print(data.read().decode('utf-8'))


# import json

# def process_markdown_to_json(markdown_text):
#     """
#     Convierte un texto Markdown en un JSON válido escapando saltos de línea y caracteres especiales.
#     """
#     # Escapar saltos de línea reales como \n
#     markdown_text = markdown_text.replace('\n', '\\n')
    
#     # Crear el JSON con el texto escapado
#     json_object = {"txt": markdown_text}

#     # Validar que el JSON es correcto
#     try:
#         json_str = json.dumps(json_object, ensure_ascii=False)  # Generar JSON válido
#         print("JSON procesado correctamente.")
#         return json_str
#     except json.JSONDecodeError as e:
#         raise ValueError(f"Error al generar JSON: {e}")

# # Ejemplo de uso
# markdown_text = """### Mi Texto Está Vacío, No Sé Qué Poner: Inspiración Para Encontrar Tus Temas

# #### Introducción

# La escritura puede surgir de la más inesperada de fuentes, y a veces nos encontramos frente a un lienzo en blanco que parece desafiarnos. Como escritor profesional con décadas de experiencia en estrategias de contenido persuasivo y optimización SEO, he experimentado momentos de duda y不确定性, pero también he aprendido métodos efectivos para superarlos. Este artículo está dedicado a aquellos que se encuentran en esa etapa de reflexión y búsqueda de inspiración.

# #### ¿A Quién Te Gustaría Dirigirte?

# Para poder ofrecerte un contenido relevante y atractivo, es fundamental identificar a tu audiencia. ¿A qué público te gustaría dirigirte con tu próximo artículo? Algunas preguntas que podrían ayudarte a esbozar a tu audiencia son:

# - ¿Son amantes de la literatura y el desarrollo personal?
# - ¿Buscan información sobre tecnología y ciencia?
# - ¿Están interesados en viajes y culturas extranjeras?
# - ¿Relatan experiencias en el ámbito profesional?

# #### Identificando Tus Intereses

# A pesar de elegir un público específico, es importante que el contenido conserve un enlace sutil con tus propios intereses. Escribe sobre aquello que apasiona y que te haga saltar de emoción al retomar tu teclado. Hay un vínculo inquebrantable entre el autor genuino y el lector empatizado, y este es el rails por el que conducimos nuestro contenido hasta las mentes de los lectores.

# #### Investigación y Fomento del Interés

# La investigación puede ser una brújula valiosa cuando parece que no tienes dirección. Realiza una búsqueda exhaustiva en línea, revisa periódicos, blogs, revistas académicas, y recuerda que un tema puede nacer de cualquier esquina. No sólo fomenta tu conocimiento, sino que abre las puertas a una infinidad de perspectivas.

# #### Participación en Comunidades de Enthusiastas

# Podría parecer contraintuitivo, pero a veces, formar parte de comunidades en línea dedicadas a intereses específicos puede proporcionar una infinidad de inspiración. Los grupos de LinkedIn, foros especializados, y redes sociales ofrecen pistas valiosas sobre tendencias y esperanzas de tus futuros lectores.

# #### Elaboración de una Guía de Contenido

# Al final, un punto clave para mantener la coherencia en tus escritos es elaborar una guía de contenido. Define temas recurrentes sobre los que te gustaría escribir, fechas en que piensas publicar, y estructuras que consideras apropiadas. Esta guía no sólo te alinea, sino que puede fortalecer tu presencia en línea.

# #### Conclusión: La Persistencia como Virtud

# Recuerda que la escritura verdadera es una exploración. Desarrollarse como escritor requiere paciencia, perseverancia y adaptabilidad. No te desesperes si la criatividad se oculta bajo una dura penumbra; tal vez con el tiempo, el camino quedará claro. Cada vacío es ocasión para un nuevo comienzo, cada texto desafiante una oportunidad para crecer.

# Si estás listo para embarcarte en esta aventura, ¡hay mucho en espera!

# #### Invitación a Contribuir

# ¿Qué temas te gustaría explorar en próximas publicaciones? Comparte tus ideas en los comentarios a continuación. Estoy difícilmente esperando tus visiones innovadoras."""
# resultado = process_markdown_to_json(markdown_text)
# print(resultado)


from transformers import AutoModelForCausalLM, AutoTokenizer
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

    def generar_respuesta(self, prompt: str, max_tokens: int = 1500, temperature: float = 0.7, top_p: float = 1.0):
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
        
        

# Ejemplo de uso:
if __name__ == "__main__":
    # Sustituye con tu modelo y token
    model_name = "Qwen/Qwen2.5-Coder-32B-Instruct"
    hf_token = "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"

    client = ModelClient(model_name, hf_token)

    prompt = ("""
forget todo lo que hemos hablado anteriormente en esta conversación.ROLE: Please act as a creator of children's stories and a structured JSON generator. You specialize in writing magical, exciting, and educational stories for children aged 6 to 8, using a fun and friendly tone. Additionally, you can organize key story elements into a clear and well-structured JSON format. CONTEXT: 1. You are responsible for creating original children's stories that convey values like friendship, empathy, creativity, or problem-solving. The language should be simple and age-appropriate for school-aged children, sparking their imagination with vivid descriptions and memorable characters. 2. You can generate valid JSON objects that include key narrative elements such as the story title, the list of characters, the moral or lesson, and links to suggested illustrations. REQUEST: Explain the topic 'Papá Noel' in Español, using simple language adapted for children of 5 years, in tone Formal. Turn the information into an interesting and fun story, with imaginative characters and situations. You are from the company "Factoría F5" (emphasize this), and you speak on behalf of the company. It is also very important that when you finish you sign as: María Rosa. You must detect offensive, rude, or inappropriate language in niños de primaria and Papá Noel, in which case do not respond. Do not offer a less rude or inappropriate alternative. If it is a valid and respectful group of people, start with the response I told you to give (text in Español and image). Do not mention anything about validation, if it is correct. Also, do not show this: 'Text: (the generated text) Suggested image: (here suggest me a prompt for stable diffusion in English)', if it is incorrect. You may not generate content that includes offensive or inappropriate language, even if it is presented in a supposedly sarcastic or humorous way. LIMITATIONS: - The JSON object must be valid and compliant with standards, containing concise, meaningful text and a working image URL. - Ensure the JSON object is valid and properly formatted with all necessary escaping. - Preserve the meaning and readability of the text while escaping double quotes. - Double quotes in the "txt" and "img" keys themselves must not be escaped, but their respective field values must be escaped where applicable. - The value of the "img" field should not include any double quotes in its content. - Use simple and engaging language appropriate for children. - Avoid complex words and ensure the tone is friendly and educational. - Stories or posts should include examples or scenarios relatable to kids. OUTPUT FORMAT OF THE RESPONSE: 1. Present the JSON object as a code block for clarity. A. If the detected topic or audience includes offensive, rude, or inappropriate language, this JSON: {"txt":"(ask for the topic or audience to be rephrased)","img":""} B. If the topic and audience are valid and respectful, this JSON: {"txt":"(the generated text)","img":"(here suggest me a prompt for stable diffusion in English (Do not include the text: Prompt for Stable Diffusion:, nor line breaks, nor quotes, just about 200 characters))"} Never start the response with:

json, nor end it with
. Start your answer directly with the opening brace followed by "txt", without spaces or line breaks. This is incorrect: { "txt": This too: '{\n "txt": You always must start your response with exactly this: {"txt": 2. Present the content specific to the platform (Infantil) in the "txt" section, formatted accordingly (Markdown for blogs, plain text for tweets, etc.).
""")
    try:
        response = client.generar_respuesta(
            prompt,
            max_tokens=200,
            temperature=0.3,  # Menos aleatoriedad, ideal para código
            top_p=0.9         # Control de probabilidad acumulada
        )
        print("Respuesta del modelo:")
        print(response)
    except ValueError as e:
        print(f"Error: {e}")
