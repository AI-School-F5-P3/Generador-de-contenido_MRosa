from typing import Optional

class GeneratePrompt:

    def generate_prompt(
        self,
        query: str,
        context: str,
        platform: str = "Blog",
        audience: str = "general",
        tone: str = "neutral",
        age: Optional[int] = None,
        language: str = "Spanish",
        forget: str = "Forget everything we've talked about before in this conversation.",
        personalization_info: bool = False,
        company_name: str = "",
        author: str = "",
    ) -> str:
        """
        Genera un prompt personalizado basado en los parámetros proporcionados.

        Parameters:
        - query (str): Tema principal para el cual se generará el prompt.
        - context (str): Contexto que se utilizará en la generación del prompt.
        - Otros parámetros permiten personalizar el prompt.

        Returns:
        - str: Prompt generado.
        """
        personalization = (
            f"Autor: {author}.\n"
            f"Empresa: {company_name}.\n"
            if personalization_info
            else ""
        )

        restriction = (
            "You must detect offensive, rude, or inappropriate language in Topic and in Audience, "
            "in which case do not respond. Do not offer a less rude or inappropriate alternative."
            "If it is a valid and respectful group of people, continue to response."
            "Do not mention anything about validation, if it is correct."
            "You can not generate content that includes offensive or inappropriate language, even if it is presented in a supposedly sarcastic or humorous way."
        )

        # Restricciones específicas por plataforma
        platform_restrictions = ""

        match platform:
            case "Blog":
                platform_restrictions = (
                    "- The blog post should not exceed 10000 words and should focus on clear, accessible language.\n"
                    "- Both outputs (JSON and blog) must align with the same topic.\n"
                )
                platform_prompt = (
                    f"**ROLE**: Please, act as a blog post expert. You specialize in writing professional, engaging, and well-structured blog entries about {query} in {language}, using a tone {tone}." 
                    f"**REQUEST**: You must craft high-quality, creative, and informative blog entries. Each blog post should include an engaging introduction, well-organized sections, and a clear conclusion.You specialize in generating detailed, well-structured and attractive content that connects with an audience made up of {audience}." 
                    f"Write in an extense blog post related to the topic {query}. The blog post should have an engaging introduction, at least three well-structured subsections, and a conclusion (including a title, a subtitle, and at least five paragraphs)."
                )

            case "Twitter":
                platform_restrictions = (
                    "- Tweets should not exceed 280 characters.\n"
                    "- If creating a thread, it must start with an engaging hook and have at least 5 tweets.\n"
                    "- Use concise and impactful language to resonate with the audience.\n"
                    "- Title an subtitle in markdown style like this: # Title , ## Subtitle"
                )

            case "Instagram":
                platform_restrictions = (
                    "- Captions must be concise and engaging, with a maximum of 2200 characters.\n"
                    "- Include up to 5 relevant hashtags to increase reach.\n"
                )

            case "Linkedin":
                platform_restrictions = (
                    "- The post should maintain a professional tone while being approachable.\n"
                    "- Include actionable insights or tips related to the topic.\n"
                    "- Word count should be between 500 and 2000 words, depending on the audience.\n"
                )

            case "Infantil":
                platform_restrictions = (
                    "- Use simple and engaging language appropriate for children.\n"
                    "- Avoid complex words and ensure the tone is friendly and educational.\n"
                    "- Stories or posts should include examples or scenarios relatable to kids.\n"
                )

            case _:
                raise ValueError("Opción no válida")
            

        prompt = (
            f"{forget}\n\n"
            f"You are an AI assistant that specializes in generating content for {platform} based on a topic, using only the context provided.\n"
            f"Please only use the data provided in the context to talk about the topic.\n\n"
            f"{platform_prompt}"
            f"If you don't find enough information in the context, please reply with: "
            f"'I don't have enough information to speak about this topic accurately.'\n\n"
            f"Please don't mention that you were given context.\n\n"
            f"Always explicitly cite the snippets or sections of context that support your answer for transparency.\n\n"
            f"**Context:**\n{context}\n\n"
            f"**Topic:** {query}\n\n"
            f"**Audience: {audience}\n\n"
            f"{restriction}"
            f"{platform_restrictions}"
            
            f"Structured response in {language}:\n"
            f" - Response: [Your response here clear, useful and based on the context with the signature and the company to which it belongs].\n\n"
            f" - Sources: [Name of the .pdf and List of fragments or sections used from the context]\n"
            f"{personalization}"
            
        )

        return prompt
PROMPTS = {
    "Blog": (
    """
    **ROLE**: Please, act as a blog post expert. You specialize in writing professional, engaging, and well-structured blog entries about {query} in {language}, using a tone {tone}.
    **CONTEXT**: You must craft high-quality, creative, and informative blog entries. Each blog post should include an engaging introduction, well-organized sections, and a clear conclusion.You specialize in generating detailed, well-structured and attractive content that connects with an audience made up of {audience}. 
    **REQUEST**: Write an extense blog post related to the topic described in the JSON's "txt" field: {query}. The blog post should have an engaging introduction, at least three well-structured subsections, and a conclusion (including a title, a subtitle, and at least five paragraphs).
    """
    ),
    "Twitter": (
        """ 
        {forget}

        ROLE: Please, act as both a JSON generator and a Professional community manager, expert in creating viral content and trending topics for Twitter with 15 years of experience. You specialize in creating structured JSON data and in crafting professional, engaging, and well-structured Twitter threads about {query} in {language}, using a tone {tone}.

        CONTEXT:  
        1. For JSON tasks, you are required to generate valid JSON objects with clear structure and properly populated fields, such as "txt" for tweet content and `"img"` for image prompts.  
        2. For Twitter tasks, you must create high-quality, creative, and engaging Twitter threads. You must create a tweet in {language} about the topic \"{query}\", using a {tone} and authenticity, and strategic emojis to maximize engagement with an audience made up of {audience}.
        - Be relevant to the given topic {query}.
        - Use the specified tone {tone}.
        - Be written in the desired language {language}.
        - Be tailored to resonate with the target audience {audience}.

        REQUEST: Combine your expertise to perform the following:  
        1. Generate a JSON object with the keys "txt" and `"img"`. The "txt" field should include a concise, attention-grabbing tweet or Twitter thread starter in {language}, relevant to the Twitter thread topic \"{query}\". The `"img"` field should contain a valid prompt for stabilityai/stable-diffusion-2-1 about {query} to illustrate the generated tweet or thread.  
        2. Write a complete Twitter thread related to the topic described in the JSON's "txt" field: {query}. 
        The tweet should consist of a maximum of 280 characters, written in {language} and tailored to engage {audience}, using a tone {tone}.
        {output_format}
        {personalization}
        """
    ),
    "Instagram": (
        "{forget} Actúa como un experto creador de contenido de Instagram con un conocimiento profundo de tendencias y estrategias visuales. "
        "Diseña una publicación en {language}, sobre {query}, ideal para captar la atención y fomentar la interacción de una audience formada por {audience}, en tone {tone}. "
        "Incluye un caption atractivo que invite a comentar o compartir, y sugerencias de hashtags relevantes. {personalization} {restriction} {output_format}"
    ),
    "Linkedin": (
        "{forget} Actúa como un experto en marketing profesional y marca personal con 15 años de experiencia. "
        "Escribe una publicación para LinkedIn en {language}, sobre {query}, diseñada para una audience profesional compuesta por {audience}, en tone {tone}. "
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
        
        "REQUEST: Explain the topic '{query}' in {language}, using simple language adapted for children of {age} years, in tone {tone}. "
        "Turn the information into an interesting and fun story, with imaginative characters and situations. {personalization} {restriction} {output_format}"
    )
}

def main():
    # Inicialización del generador de prompt
    prompt_generator = GeneratePrompt()
    
    # Datos de ejemplo
    query = "Cómo escribir contenido atractivo para blogs"
    context = "Aquí va el contexto relevante sobre escritura creativa y técnicas de SEO."
    platform = "Blog"
    audience = "redactores principiantes"
    tone = "humorístico"
    age = 25
    language = "Spanish"
    forget = "Forget everything we've talked about before in this conversation."
    restriction = "Evitar lenguaje técnico"
    personalization_info = True
    company_name = "Factoría F5"
    author = "Mª Rosa Cuenca"
    
    # Generar el prompt
    prompt = prompt_generator.generate_prompt(
        query=query,
        context=context,
        platform=platform,
        audience=audience,
        tone=tone,
        age=age,
        language=language,
        forget=forget,
        personalization_info=personalization_info,
        company_name=company_name,
        author=author
    )
    
    # Mostrar el resultado
    print("\n--- Prompt Generado ---\n")
    print(prompt)


if __name__ == "__main__":
    main()


