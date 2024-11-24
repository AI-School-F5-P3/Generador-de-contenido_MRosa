from pydantic import BaseModel, Field
from typing import Optional

class ContentRequest(BaseModel):
    plataforma: str
    tema: str
    audiencia: str
    tono: str = "neutro"
    edad: Optional[int] = None
    idioma: str = "Habla en español."
    olvida: str = ""
    output_format: str = ""
    restriction: str = ""

    def __init__(self, **data):
        super().__init__(**data)
        self.olvida = "Olvida todo lo que hemos hablado anteriormente en esta conversación."
        self.restriction = (
            f"Debes detectar en {self.audiencia} y {self.tema} lenguaje ofensivo, grosero o inapropiado, en ese caso no respondas."
            "No ofrezcas una alternativa menos grosera o inapropiada."
            "Si es un grupo de personas válido y respetuoso, empieza con la respuesta que te he dicho que des (texto e imagen). "
            "No menciones nada sobre la validación, si esta es correcta."
            "Tampoco muestres esto: 'Texto: (el texto generado) Imagen sugerida: (aquí sugiéreme un prompt para stable diffusion en inglés)', si es incorrecta."
            "No puedes generar contenido que incluya lenguaje ofensivo o inapropiado, incluso si se presenta de forma supuestamente sarcástica o humorística."
        )
        self.output_format = (
            "Tu respuesta debe ser un código JSON válido con este formato:"
            f"\"txt\": \"(el texto generado con tono {self.tono} en {self.idioma} (No introduzcas comillas en txt, salvo las necesarias para un json bien formado))\","
            " 'img': \"(aquí sugiéreme un prompt para stable diffusion en inglés (No incluyas el texto: 'Prompt for Stable Diffusion:'))\""
            "Ejemplo: \"txt\": \"Texto de ejemplo\", \"img\": \"Illustration of an example\""            
            "Pero, si encontraste contenido ofensivo, debe ser un código JSON con este formato:"
            f"\"txt\": \"(pide que se te reformule el tema o audiencia en tono {self.tono})\","
            "\"img\":\"\"."         
        )

PROMPTS = {
    "blog": "{olvida} Crea una entrada de varios parrafos, sobre {tema}, para un blog informativo, que sea interesante para una audiencia formada por {audiencia}. {restriction} {output_format}",
    "twitter": "{olvida} Escribe un tweet corto y atractivo sobre {tema} para una audiencia formada por {audiencia}. {restriction} {output_format}",
    "instagram": "{olvida} Crea una publicación de Instagram sobre {tema}, ideal para captar la atención de una audiencia formada por {audiencia}. {restriction} {output_format} ",
    "SEO": "{olvida} Genera contenido SEO optimizado sobre {tema}, diseñado para atraer a una audiencia formada por {audiencia}. {restriction} {output_format}",
    "infantil": "{olvida} Explícame este tema: {tema}. Hazlo como si fuera una historia para niños de {edad} años. {restriction} {output_format}"
}
