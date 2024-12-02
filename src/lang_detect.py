from langdetect import detect, DetectorFactory

class DetectorDeIdioma:
    def __init__(self):
        # Establecer una semilla para obtener resultados consistentes
        DetectorFactory.seed = 0

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
            return f"Error en la detección: {e}"

# Ejemplo de uso
if __name__ == "__main__":
    detector = DetectorDeIdioma()
    texto_entrada = "Texto en el idioma de origen"
    idioma_origen = detector.detectar_idioma(texto_entrada)
    print(idioma_origen)  # Esto imprimirá el código del idioma detectado, por ejemplo, 'es' para español
