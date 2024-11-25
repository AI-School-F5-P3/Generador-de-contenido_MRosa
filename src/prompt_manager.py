from pydantic import BaseModel, Field, model_validator
from typing import Optional

class ContentRequest(BaseModel):
    plataforma: str
    tema: str = "No se que escribir"
    audiencia: str = "generalista"
    tono: str = "neutro"
    edad: Optional[int] = None
    idioma: str = "Español"
    olvida: str = "Olvida todo lo que hemos hablado anteriormente en esta conversación." 
    output_format: str = Field(default="")
    restriction: str = Field(default="")

    @model_validator(mode="before")
    @classmethod
    def validar_campos(cls, values):
        """
        Valida y corrige campos antes de inicializar el modelo.
        """
        if not values.get('tema', '').strip():
            values['tema'] = "Mi texto esta vacío, no sé que poner. Pregúntame sobre que quiero hablar. "
        if not values.get('audiencia', '').strip():
            values['audiencia'] = "No sé a quien dirigirme. Pregúntame a quien me quiero dirigir."
        return values

    def __init__(self, **data):
        super().__init__(**data)
        self.restriction = (
            f"Debes detectar en {self.audiencia} y {self.tema} lenguaje ofensivo, grosero o inapropiado, en ese caso no respondas."
            "No ofrezcas una alternativa menos grosera o inapropiada."
            f"Si es un grupo de personas válido y respetuoso, empieza con la respuesta que te he dicho que des (texto en {self.idioma} e imagen). "
            "No menciones nada sobre la validación, si esta es correcta."
            "Tampoco muestres esto: 'Texto: (el texto generado) Imagen sugerida: (aquí sugiéreme un prompt para stable diffusion en inglés)', si es incorrecta."
            "No puedes generar contenido que incluya lenguaje ofensivo o inapropiado, incluso si se presenta de forma supuestamente sarcástica o humorística."
        )
        self.output_format = (
            "Tu respuesta debe ser un código JSON válido con este formato:"
            f"{{\"txt\": \"(el texto generado (en {self.idioma}) con tono {self.tono} (No introduzcas comillas en txt, salvo las necesarias para un JSON bien formado))\","
            "\"img\": \"(aquí sugiéreme un prompt para stable diffusion en inglés (No incluyas el texto: 'Prompt for Stable Diffusion:', ni saltos de línea, ni comillas))\"}}"
            " Ejemplo: {\"txt\": \"Texto de ejemplo\", \"img\": \"Illustration of an example\"}."            
            " Pero, si encontraste contenido ofensivo, debe ser un código JSON con este formato:"
            f"{{\"txt\": \"(pide que se te reformule el tema o audiencia en tono {self.tono})\","
            "\"img\": \"\"}}."
        )


PROMPTS = {
    "blog": "{olvida} Crea una entrada de varios parrafos, sobre {tema}, para un blog informativo en {idioma}, que sea interesante para una audiencia formada por {audiencia}. {restriction} {output_format}",
    "twitter": "{olvida} Escribe un tweet corto y atractivo en {idioma}, sobre {tema} para una audiencia formada por {audiencia}. {restriction} {output_format}",
    "instagram": "{olvida} Crea una publicación de Instagram en {idioma}, sobre {tema}, ideal para captar la atención de una audiencia formada por {audiencia}. {restriction} {output_format} ",
    "SEO": "{olvida} Genera contenido SEO optimizado en {idioma}, sobre {tema}, diseñado para atraer a una audiencia formada por {audiencia}. {restriction} {output_format}",
    "infantil": "{olvida} Explícame este tema en {idioma}: {tema}. Hazlo como si fuera una historia para niños de {edad} años. {restriction} {output_format}"
}
