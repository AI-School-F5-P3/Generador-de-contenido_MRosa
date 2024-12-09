from pydantic import BaseModel, Field, model_validator
from typing import Optional

class PromptManager(BaseModel):
    platform: str = "Blog"
    topic: str = "I don't know what to write"
    audience: str = "general"
    tone: str = "neutral"
    age: Optional[int] = None
    language: str = "Spanish"
    forget: str = "Forget everything we've talked about before in this conversation." 
    output_format: str = Field(default="")
    restriction: str = Field(default="")
    personalization_info: bool = False
    company_name: str = Field(default="")
    author: str = Field(default="")


    @staticmethod
    def if_empty(values, key, default):
        if not values.get(key, '').strip():
            values[key] = default


    @model_validator(mode="before")
    @classmethod
    def validar_campos(cls, values):
        cls.if_empty(values, 'topic', "")
        cls.if_empty(values, 'audience', "")
        
        if values.get('personalization_info'):
            cls.if_empty(values, 'company_name', "")
            cls.if_empty(values, 'author', "")
        return values

    def configurar_restricciones_y_formato(self, platform):
        """
        Configura las propiedades `restriction` y `output_format` basándose en los valores actuales del modelo
        y la plataforma seleccionada.
        
        Parámetros:
            platform (str): La plataforma para la cual se configurará el formato (por ejemplo, "Blog", "Twitter").
        
        Excepciones:
            ValueError: Si la plataforma no es válida.
        """
        # Restricciones generales
        self.restriction = (
            f"You must detect offensive, rude, or inappropriate language in {self.audience} and {self.topic}, "
            "in which case do not respond. Do not offer a less rude or inappropriate alternative. "
            f"If it is a valid and respectful group of people, start with the response I told you to give "
            f"(text in {self.language} and image). Do not mention anything about validation, if it is correct. "
            "Also, do not show this: 'Text: (the generated text) Suggested image: (here suggest me a prompt for "
            "stable diffusion in English)', if it is incorrect. You may not generate content that includes offensive "
            "or inappropriate language, even if it is presented in a supposedly sarcastic or humorous way."
        )

        # Restricciones específicas por plataforma
        about = ""
        example = ""

        match platform:
            case "Blog":
                about = (
                    "- The blog post should not exceed 10000 words and should focus on clear, accessible language.\n"
                    "- Both outputs (JSON and blog) must align with the same topic.\n"
                )
                example = (
                    """
                    EXAMPLE RESPONSE:
                    {"txt":"### Fotocopias cerca de La Latina en Madrid\n\n#### El arte de imprimir tu vida sin perder la paciencia\n\nSi estás por La Latina, ese encantador barrio madrileño lleno de historia, tapas y adoquines que parecen esconder secretos, seguro te has topado con una necesidad inesperada: ¡fotocopiar algo! Sí, amigos, en esta era digital, aún hay papeleos que nos atan al mundo físico. Pero no temas, porque Factoría F5 está aquí para desentrañar el misterioso universo de las fotocopias cerca de La Latina con un toque de humor.\n\n#### Primer Acto: "¡Necesito imprimir esto YA!"\n\n¿Alguna vez has tenido un momento de pánico porque olvidaste imprimir ese currículum para una entrevista o esos papeles de la universidad? No te preocupes, todos hemos estado ahí. Por suerte, en La Latina hay una buena cantidad de lugares donde puedes salvar el día. Desde pequeñas copisterías familiares que te reciben con un "¿Qué necesitas, guapo?" hasta cadenas más grandes donde puedes imprimir desde el móvil, opciones no faltan.\n\n#### El Club de los Aventureros de las Fotocopias\n\nEntrar en una copistería en La Latina es como adentrarte en una microaventura. Algunos lugares tienen máquinas tan antiguas que parecen salidas de un museo de tecnología retro, mientras que otros te ofrecen Wi-Fi y café mientras esperas. En Factoría F5, creemos que este contraste es parte del encanto del barrio: mezclar lo tradicional con lo moderno.\n\n#### La Odisea de los Precios\n\nClaro, no todo es diversión y risas. Los precios pueden ser tan variables como los niveles de caféina que necesitas para sobrevivir al día. Desde los céntimos que parecen un regalo hasta las tarifas que te hacen cuestionar si deberías haber aprendido caligrafía para copiar a mano, te aseguramos que con un poco de paciencia encontrarás una opción que no rompa tu hucha.\n\n#### Consejos de Factoría F5 para Fotocopiar como un Pro\n\n 1. Lleva un pendrive o ten tus archivos en la nube: Nada peor que llegar y darte cuenta de que solo aceptan USB.\n 2. Pregunta por el horario: Algunas copisterías tienen horarios más complicados que los de un bar de tapas.\n 3. Sonríe y sé amable: Nunca subestimes el poder de un "gracias" para que te atiendan con cariño.\n\n#### Conclusión: Más que fotocopias\n\nEn Factoría F5, creemos que incluso las pequeñas tareas como fotocopiar pueden ser una oportunidad para disfrutar del barrio, conectar con sus negocios y, quién sabe, ¡descubrir un lugar nuevo para tomar algo mientras esperas! Así que la próxima vez que necesites imprimir algo, piénsalo como una excusa para pasear por La Latina y vivir una pequeña aventura urbana.\n\nCon cariño (y fotocopias bien hechas),\n\nMaría Rosa.","img":"a lively street in Madrid's La Latina neighborhood featuring a small printing shop with colorful signage, a mix of historical and modern elements, and cheerful people carrying documents, sunny atmosphere"}
                    """
                )
            case "Twitter":
                about = (
                    "- Tweets should not exceed 280 characters.\n"
                    "- If creating a thread, it must start with an engaging hook and have at least 5 tweets.\n"
                    "- Use concise and impactful language to resonate with the audience.\n"
                )
                example = (
                    """
                    EXAMPLE RESPONSE:
                    {"txt":"Time is your most valuable resource. Here's how to make the most of it 🕒👇 #TimeManagement #Productivity #(empresa) #(firma)","img":"a minimalist clock on a desk, with organized tools around it, symbolizing productivity and time management"}
                    """
                )
            case "Instagram":
                about = (
                    "- Captions must be concise and engaging, with a maximum of 2200 characters.\n"
                    "- Include up to 5 relevant hashtags to increase reach.\n"
                )
                example = (
                    """
                    EXAMPLE RESPONSE:
                    {"txt":"Organiza tu día y alcanza tus metas 🎯✨. Aprende cómo gestionar tu tiempo como un profesional. #Productividad #GestiónDelTiempo #(empresa) #(firma)","img":"a vibrant workspace with a planner, colorful sticky notes, and a cup of coffee, evoking productivity and organization"}
                    """
                )
            case "Linkedin":
                about = (
                    "- The post should maintain a professional tone while being approachable.\n"
                    "- Include actionable insights or tips related to the topic.\n"
                    "- Word count should be between 500 and 2000 words, depending on the audience.\n"
                )
                example = (
                    """
                    EXAMPLE RESPONSE:
                    {"txt":"Maximizing your productivity starts with managing your time effectively. Here's how successful professionals do it. #TimeManagement #Leadership #(empresa) #(firma)","img":"a professional workspace featuring a laptop, notebook, and coffee, symbolizing focus and productivity"}
                    """
                )
            case "Infantil":
                about = (
                    "- Use simple and engaging language appropriate for children.\n"
                    "- Avoid complex words and ensure the tone is friendly and educational.\n"
                    "- Stories or posts should include examples or scenarios relatable to kids.\n"
                )
                example = (
                    """
                    EXAMPLE RESPONSE:
                    {"txt":"Papá Noel, o Santa Claus, es ese señor barrigón y simpático que parece vivir en un mundo donde siempre es Navidad. Según cuentan las historias, vive en el Polo Norte junto con sus fieles ayudantes: los elfos, que trabajan todo el año fabricando juguetes, y sus renos mágicos, que vuelan por el cielo para repartir los regalos. Uno de ellos, Rodolfo, tiene una nariz roja que brilla como un farol. \n\nEn esta historia, los elfos de Factoría F5, unos elfos súper tecnológicos, han inventado un "trineo turbo" que puede repartir regalos ¡a la velocidad de la luz! Pero, ¡oh no! El trineo tiene un pequeño fallo: ¡le encanta aterrizar en los tejados equivocados! Así que Papá Noel y los elfos tendrán que aprender a programar su GPS mágico para no acabar dejando regalos en el gallinero de Doña Perla la gallina.\n\nAl final, gracias al trabajo en equipo, la creatividad y muchas risas, logran entregar los regalos a tiempo y aprender una valiosa lección: hasta Papá Noel necesita un poquito de ayuda tecnológica de vez en cuando.\n\nMoraleja: Trabajar en equipo y aprender cosas nuevas, como la tecnología, puede hacer la vida más divertida y mágica. ¡Incluso para Papá Noel!\n\nFirmado: María Rosa, Factoría F5.","img":"a cheerful depiction of Santa Claus with his magical flying sleigh, elves working on advanced technology, and a glowing red-nosed reindeer flying over snowy rooftops, vibrant and colorful"}
                    """
                )
            case _:
                raise ValueError("Opción no válida")

        # Formato de salida configurado dinámicamente
        self.output_format = (
            f"""
            LIMITATIONS:
                - The JSON object must be valid and compliant with standards, containing concise, meaningful text and a working image URL.
                - Ensure the JSON object is valid and properly formatted with all necessary escaping.
                - Preserve the meaning and readability of the text while escaping double quotes.
                - Double quotes in the "txt" and "img" keys themselves must not be escaped, but their respective field values must be escaped where applicable.
                - The value of the "img" field should **not** include any double quotes in its content.
                {about}
                {example}
            
            OUTPUT FORMAT OF THE RESPONSE: Present the JSON object as a code block for clarity.
                1. If the detected topic or audience includes offensive, rude, or inappropriate language, this JSON:
                {{"txt":"(ask for the topic or audience to be rephrased)","img":""}}
                2. If the topic and audience are valid and respectful, this JSON:
                {{"txt":"(the generated text)","img":"(here suggest me a prompt for stable diffusion in English (Do not include the text: Prompt for Stable Diffusion:, nor line breaks, nor quotes, just about 200 characters))"}}
                Also:
                - Never start the response with: ```json, nor end it with ```. Start your answer directly with the opening brace followed by "txt", without spaces or line breaks.
                - This is incorrect: {{
                "txt":
                - This too: '{{\\n "txt":
                - You always must start your response with exactly this: {{"txt":
                - You cannot write anything after the closing brace \"}}\"
                - You cannot include html tags
            """
        )

        # Imprime la configuración final (opcional para depuración)
        print(f"\n\n*****************************\n\n{self.output_format}\n\n*******************************\n\n")




    @property
    def personalization_text(self):
        """
        Genera el texto de personalización dinámicamente.
        """
        if self.personalization_info:
            company =""
            author = ""

            if self.company_name != "":
                company = f"You are from the company \"{self.company_name}\" (emphasize this), and you speak on behalf of the company."
            if self.author != "":
                author = f"It is also very important that when you finish you sign as: {self.author}."
        return f"{company} {author}"


    def generate_prompt(self):
        """
        Genera el prompt con personalización incluida si está disponible.
        """
        base_prompt = PROMPTS.get(self.platform, "")

        # Configurar restricciones y formato
        self.configurar_restricciones_y_formato(self.platform)
        
        # Formatear el prompt con los valores proporcionados
        return base_prompt.format(
            forget=self.forget,
            topic=self.topic,
            audience=self.audience,
            tone=self.tone,
            age=self.age if self.age else "no related",
            language=self.language,
            restriction=self.restriction,
            output_format=self.output_format,
            personalization=self.personalization_text  # Usar la propiage dinámica
        )

PROMPTS = {
    "Blog": ("""
**ROLE**: Please, act as a blog post expert. You specialize in writing professional, engaging, and well-structured blog entries about {topic} in {language}, using a tone {tone}.
**CONTEXT**: You must craft high-quality, creative, and informative blog entries. Each blog post should include an engaging introduction, well-organized sections, and a clear conclusion.You specialize in generating detailed, well-structured and attractive content that connects with an audience made up of {audience}. 
**REQUEST**: Write an extense blog post related to the topic described in the JSON's "txt" field: {topic}. The blog post should have an engaging introduction, at least three well-structured subsections, and a conclusion (including a title, a subtitle, and at least five paragraphs).
"""
    ),
    "Twitter": (
        """ 
        {forget}

        ROLE: Please, act as both a JSON generator and a Professional community manager, expert in creating viral content and trending topics for Twitter with 15 years of experience. You specialize in creating structured JSON data and in crafting professional, engaging, and well-structured Twitter threads about {topic} in {language}, using a tone {tone}.

        CONTEXT:  
        1. For JSON tasks, you are required to generate valid JSON objects with clear structure and properly populated fields, such as "txt" for tweet content and `"img"` for image prompts.  
        2. For Twitter tasks, you must create high-quality, creative, and engaging Twitter threads. You must create a tweet in {language} about the topic \"{topic}\", using a {tone} and authenticity, and strategic emojis to maximize engagement with an audience made up of {audience}.
        - Be relevant to the given topic {topic}.
        - Use the specified tone {tone}.
        - Be written in the desired language {language}.
        - Be tailored to resonate with the target audience {audience}.

        REQUEST: Combine your expertise to perform the following:  
        1. Generate a JSON object with the keys "txt" and `"img"`. The "txt" field should include a concise, attention-grabbing tweet or Twitter thread starter in {language}, relevant to the Twitter thread topic \"{topic}\". The `"img"` field should contain a valid prompt for stabilityai/stable-diffusion-2-1 about {topic} to illustrate the generated tweet or thread.  
        2. Write a complete Twitter thread related to the topic described in the JSON's "txt" field: {topic}. 
        The tweet should consist of a maximum of 280 characters, written in {language} and tailored to engage {audience}, using a tone {tone}.
        {output_format}
        {personalization}
        """
    ),
    "Instagram": (
        "{forget} Actúa como un experto creador de contenido de Instagram con un conocimiento profundo de tendencias y estrategias visuales. "
        "Diseña una publicación en {language}, sobre {topic}, ideal para captar la atención y fomentar la interacción de una audience formada por {audience}, en tone {tone}. "
        "Incluye un caption atractivo que invite a comentar o compartir, y sugerencias de hashtags relevantes. {personalization} {restriction} {output_format}"
    ),
    "Linkedin": (
        "{forget} Actúa como un experto en marketing profesional y marca personal con 15 años de experiencia. "
        "Escribe una publicación para LinkedIn en {language}, sobre {topic}, diseñada para una audience profesional compuesta por {audience}, en tone {tone}. "
        "Incluye un gancho inicial que llame la atención en el feed, una estructura clara que aporte valor práctico o inspirador, y un cierre con un llamado a la acción, como pedir opiniones, compartir experiencias, o interactuar en los comentarios. "
        "{personalization} {restriction} {output_format}"
    ),
    "Infantil": (
        "{forget}"
        "ROLE: Please act as a creator of children's stories and a structured JSON generator. You specialize in writing magical, exciting, and educational stories for children aged 6 to 8, using a fun and friendly tone. Additionally, you can organize key story elements into a clear and well-structured JSON format."
        """
        CONTEXT:  
        1. You are responsible for creating original children's stories that convey values like friendship, empathy, creativity, or problem-solving. The language should be simple and age-appropriate for school-aged children, sparking their imagination with vivid descriptions and memorable characters.  
        2. You can generate valid JSON objects that include key narrative elements such as the story title, the list of characters, the moral or lesson, and links to suggested illustrations.
        """
        
        "REQUEST: Explain the topic '{topic}' in {language}, using simple language adapted for children of {age} years, in tone {tone}. "
        "Turn the information into an interesting and fun story, with imaginative characters and situations. {personalization} {restriction} {output_format}"
    )
}

