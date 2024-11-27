import os
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

class GeneradorImagenesSD:
    def __init__(self, modelo: str = "stabilityai/stable-diffusion-2-1"):
        self.dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Usando dispositivo: {self.dispositivo}")

        self.pipeline = StableDiffusionPipeline.from_pretrained(
            modelo,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(self.pipeline.scheduler.config)
        self.pipeline.to(self.dispositivo)
        # self.pipeline.enable_attention_slicing()
        print("Generando imagen...")

    def generar_imagen(self, texto: str, archivo_salida: str = "img.png", alto: int = 100, ancho: int = 100,
                       guidance_scale: float = 6, num_steps: int = 30, semilla: int = 1175181494,
                       negative_prompt: str = "nrealfixer, nfixer, 3d render, cgi, painting, drawing, cartoon, anime"):
        try:
            alto = (alto // 64) * 64
            ancho = (ancho // 64) * 64
            generador = torch.manual_seed(semilla)

            imagen = self.pipeline(
                prompt=texto,
                negative_prompt=negative_prompt,
                height=alto,
                width=ancho,
                guidance_scale=guidance_scale,
                num_inference_steps=num_steps,
                generator=generador
            ).images[0]

            # Crear directorios automáticamente
            directorio = os.path.dirname(archivo_salida)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            imagen.save(archivo_salida)
            print(f"Imagen generada y guardada como {archivo_salida}.")
        except Exception as e:
            print(f"Error al generar la imagen: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    generador = GeneradorImagenesSD()
    texto = "portrait of a female programmer working in an office using an AI assistant, modern office environment, bright daylight, computer and tablet screens showing AI related data and algorithms"
    generador.generar_imagen(
        texto=texto,
        archivo_salida="assets/output_images/img.png",
        alto=512,
        ancho=512,
        guidance_scale=7.5,
        num_steps=10,
        semilla=1175181494,
        negative_prompt="nrealfixer, nfixer, 3d render, cgi, painting, drawing, cartoon, anime,easynegative, (low quality, worst quality:1.4), bad anatomy, bad composition, out of frame, duplicate, watermark, signature, text"
    )
