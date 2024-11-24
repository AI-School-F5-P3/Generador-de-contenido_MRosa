from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from langdetect import detect, DetectorFactory

class TraductorM2M100:
    def __init__(self, modelo: str = "facebook/m2m100_418M"):
        """
        Inicializa el traductor cargando el modelo y el tokenizador preentrenados.

        :param modelo: Nombre del modelo preentrenado en Hugging Face.
        """
        # Establecer una semilla para obtener resultados consistentes en la detección de idioma
        DetectorFactory.seed = 0
        # Cargar el tokenizador y el modelo preentrenado
        self.tokenizer = M2M100Tokenizer.from_pretrained(modelo)
        self.model = M2M100ForConditionalGeneration.from_pretrained(modelo)

    def detectar_idioma(self, texto: str) -> str:
        """
        Detecta el idioma del texto proporcionado.

        :param texto: Cadena de texto cuyo idioma se desea detectar.
        :return: Código del idioma detectado (por ejemplo, 'es' para español).
        """
        try:
            idioma = detect(texto)
            return idioma
        except Exception as e:
            raise ValueError(f"Error en la detección del idioma: {e}")

    def traducir_a_ingles(self, texto: str) -> str:
        """
        Traduce el texto proporcionado al inglés.

        :param texto: Cadena de texto en el idioma de origen.
        :return: Cadena de texto traducida al inglés.
        """
        # Detectar el idioma de origen
        idioma_origen = self.detectar_idioma(texto)
        # Configurar el tokenizador con el idioma de origen
        self.tokenizer.src_lang = idioma_origen
        # Tokenizar el texto de entrada
        encoded_input = self.tokenizer(texto, return_tensors="pt")
        # Generar la traducción al inglés
        generated_tokens = self.model.generate(
            **encoded_input,
            forced_bos_token_id=self.tokenizer.get_lang_id("en")
        )
        # Decodificar los tokens generados
        traduccion = self.tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
        return traduccion

# Ejemplo de uso
if __name__ == "__main__":
    traductor = TraductorM2M100()
    texto_entrada = "idiotas"
    traduccion = traductor.traducir_a_ingles(texto_entrada)
    print(traduccion)  # Esto imprimirá la traducción al inglés del texto proporcionado