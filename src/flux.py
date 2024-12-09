import requests
import io
from PIL import Image

# Función para generar imágenes
def generate_image(prompt, alto=512, ancho=512, guidance_scale=7.5, num_steps=50, seed=1175181494):

    try:
        API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
        headers = {"Authorization": "Bearer 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"}

        payload = {
            "inputs": prompt,
            "parameters": {
                "height": alto,
                "width": ancho,
                "guidance_scale": guidance_scale,
                "num_inference_steps": num_steps,
            }
        }

        # Añadir 'seed' si se proporciona
        if seed is not None:
            payload["parameters"]["seed"] = seed
        print("Generando imagen...")
        response = requests.post(API_URL, headers=headers, json=payload)
        print("response...")
        response.raise_for_status()  # Lanza una excepción si la solicitud falla

        image = Image.open(io.BytesIO(response.content))
        return image
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    prompt = "An analog film-style cinematic portrait of a mathematician studying in a cozy, vintage study. The mathematician is sitting at a wooden desk surrounded by chalkboards filled with handwritten equations, stacks of books, and scattered papers. Golden-hour sunlight streams through a nearby window, casting warm, soft light and dramatic shadows across the room. The scene features rich, earthy tones, a grainy texture, and a subdued color palette reminiscent of analog photography. The mathematician is lost in thought, holding a pen and gazing at their notes. The atmosphere is nostalgic, intellectual, and introspective, with a timeless, cinematic feel. Shot on 35mm analog film, with soft contrasts, depth, and warm lighting."
    alto = 300
    ancho = 300
    guidance_scale = 2
    num_steps = 3
    seed = 42
    file_name = "img.png"
    
    imagen_generada = generate_image(prompt, alto, ancho, guidance_scale, num_steps, seed)
    imagen_generada.save(file_name)
    print(f"Imagen generada y guardada como {file_name}.")
