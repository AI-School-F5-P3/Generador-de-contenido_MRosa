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
    personalization_info: bool
    company_name: str = Field(default="")
    author: str = Field(default="")

    @model_validator(mode="before")
    @classmethod
    def validar_campos(cls, values):
        if not values.get('tema', '').strip():
            values['tema'] = "Mi texto está vacío, no sé qué poner. Pregúntame sobre qué quiero hablar. "
        if not values.get('audiencia', '').strip():
            values['audiencia'] = "No sé a quién dirigirme. Pregúntame a quién me quiero dirigir."
        if not values.get('company_name', '').strip():
            values['company_name'] = "Desconozco la empresa para la que se escribe este texto. Pregúntame quién ha sido."
        if not values.get('author', '').strip():
            values['author'] = "Desconozco quién debe figurar como autor/a o autores/as. Pregúntame quién ha sido."
        return values

    def configurar_restricciones_y_formato(self):
        """
        Configura las propiedades `restriction` y `output_format` basándose en los valores actuales del modelo.
        """
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
    @property
    def personalization_text(self):
        """
        Genera el texto de personalización dinámicamente.
        """
        if self.personalization_info:
            return f"Eres de la empresa: {self.company_name}. y debes firmar como: {self.author}. "
        return ""

    def generate_prompt(self):
        """
        Genera el prompt con personalización incluida si está disponible.
        """
        base_prompt = PROMPTS.get(self.plataforma, "")
        if not base_prompt:
            raise ValueError(f"Plataforma no soportada: {self.plataforma}")
        # Configurar restricciones y formato
        self.configurar_restricciones_y_formato()
        
        # Formatear el prompt con los valores proporcionados
        return base_prompt.format(
            olvida=self.olvida,
            tema=self.tema,
            audiencia=self.audiencia,
            tono=self.tono,
            edad=self.edad if self.edad else "no especificada",
            idioma=self.idioma,
            restriction=self.restriction,
            output_format=self.output_format,
            personalization=self.personalization_text  # Usar la propiedad dinámica
        )


PROMPTS = {
    "Blog": (
        "{olvida} Actúa como un blogger profesional con 15 años de experiencia que domina estrategias de escritura persuasiva y optimización SEO. "
        "Crea una entrada detallada, bien estructurada y atractiva, sobre {tema}, para un blog informativo en {idioma}, dirigido a una audiencia compuesta por {audiencia}, en tono {tono}. "
        "Asegúrate de incluir un gancho inicial, subtítulos relevantes, y un cierre que motive a la acción o reflexión. {personalization} {restriction} {output_format}"
    ),
    "Twitter": (
        "{olvida} Actúa como un influencer experto en crear contenido viral y trending topic con 15 años de experiencia. "
        "Escribe un tweet breve, impactante y atractivo en {idioma}, sobre {tema}, diseñado para captar la atención inmediata de una audiencia formada por {audiencia}, en tono {tono}. "
        "Utiliza un tono auténtico y emojis estratégicos para maximizar el engagement. {personalization} {restriction} {output_format}"
    ),
    "Instagram": (
        "{olvida} Actúa como un experto creador de contenido de Instagram con un conocimiento profundo de tendencias y estrategias visuales. "
        "Diseña una publicación en {idioma}, sobre {tema}, ideal para captar la atención y fomentar la interacción de una audiencia formada por {audiencia}, en tono {tono}. "
        "Incluye un caption atractivo que invite a comentar o compartir, y sugerencias de hashtags relevantes. {personalization} {restriction} {output_format}"
    ),
    "Linkedin": (
        "{olvida} Actúa como un experto en marketing profesional y marca personal con 15 años de experiencia. "
        "Escribe una publicación para LinkedIn en {idioma}, sobre {tema}, diseñada para una audiencia profesional compuesta por {audiencia}, en tono {tono}. "
        "Incluye un gancho inicial que llame la atención en el feed, una estructura clara que aporte valor práctico o inspirador, y un cierre con un llamado a la acción, como pedir opiniones, compartir experiencias, o interactuar en los comentarios. "
        "{personalization} {restriction} {output_format}"
    ),
    "SEO": (
        "{olvida} Actúa como un experto en SEO y marketing de contenido con 15 años de experiencia. "
        "Genera un contenido optimizado para motores de búsqueda en {idioma}, sobre {tema}, dirigido a atraer a una audiencia formada por {audiencia}, en tono {tono}. "
        "Asegúrate de incluir palabras clave relevantes, encabezados jerárquicos y una meta descripción impactante. {personalization} {restriction} {output_format}"
    ),
    "Infantil": (
        "{olvida} Actúa como un escritor creativo especializado en historias infantiles. "
        "Explica el tema '{tema}' en {idioma}, utilizando un lenguaje sencillo y adaptado para niños de {edad} años, en tono {tono}. "
        "Convierte la información en una historia interesante y divertida, con personajes y situaciones imaginativas. {personalization} {restriction} {output_format}"
    )
}

