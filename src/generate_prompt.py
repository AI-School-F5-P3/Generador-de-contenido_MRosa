from typing import Optional

class GeneratePrompt:

    def generate_prompt(
        self,
        query: str,
        platform: str = "",
        audience: str = "",
        tone: str = "",
        age: Optional[int] = None,
        language: str = "Spanish",
        personalization_info: bool = False,
        company_name: str = "",
        author: str = "",
    ) -> str:
        """
        Genera un prompt personalizado basado en los parámetros proporcionados.

        Returns:
        - str: Prompt generado.
        """

        forget = "Forget everything we've talked about before in this conversation."

        personalization = ""
        if personalization_info:
            personalization = (
                f"Autor: {author}.\n"
                f"Empresa: {company_name}.\n"
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
                )
                platform_prompt = (
                    f"**ROLE**: Please, act as a blog post expert. You specialize in writing professional, engaging, and well-structured blog entries about {query} in {language}, using a tone {tone}." 
                    f"**REQUEST**: You must craft high-quality, creative, and informative blog entries. Each blog post should include an engaging introduction, well-organized sections, and a clear conclusion.You specialize in generating detailed, well-structured and attractive content that connects with an audience made up of {audience}." 
                    f"Write in an extense blog post related to the topic {query}. The blog post should have an engaging introduction, at least three well-structured subsections, and a conclusion (including a title, a subtitle, and at least five paragraphs)."
                )
                example = ("**EXAMPLE RESPONSE**: ### Fotocopias cerca de La Latina en Madrid\n\n#### El arte de imprimir tu vida sin perder la paciencia\n\nSi estás por La Latina, ese encantador barrio madrileño lleno de historia, tapas y adoquines que parecen esconder secretos, seguro te has topado con una necesidad inesperada: ¡fotocopiar algo! Sí, amigos, en esta era digital, aún hay papeleos que nos atan al mundo físico. Pero no temas, porque Factoría F5 está aquí para desentrañar el misterioso universo de las fotocopias cerca de La Latina con un toque de humor.\n\n#### Primer Acto: '¡Necesito imprimir esto YA!'\n\n¿Alguna vez has tenido un momento de pánico porque olvidaste imprimir ese currículum para una entrevista o esos papeles de la universidad? No te preocupes, todos hemos estado ahí. Por suerte, en La Latina hay una buena cantidad de lugares donde puedes salvar el día. Desde pequeñas copisterías familiares que te reciben con un '¿Qué necesitas, guapo?' hasta cadenas más grandes donde puedes imprimir desde el móvil, opciones no faltan.\n\n#### El Club de los Aventureros de las Fotocopias\n\nEntrar en una copistería en La Latina es como adentrarte en una microaventura. Algunos lugares tienen máquinas tan antiguas que parecen salidas de un museo de tecnología retro, mientras que otros te ofrecen Wi-Fi y café mientras esperas. En Factoría F5, creemos que este contraste es parte del encanto del barrio: mezclar lo tradicional con lo moderno.\n\n#### La Odisea de los Precios\n\nClaro, no todo es diversión y risas. Los precios pueden ser tan variables como los niveles de caféina que necesitas para sobrevivir al día. Desde los céntimos que parecen un regalo hasta las tarifas que te hacen cuestionar si deberías haber aprendido caligrafía para copiar a mano, te aseguramos que con un poco de paciencia encontrarás una opción que no rompa tu hucha.\n\n#### Consejos de Factoría F5 para Fotocopiar como un Pro\n\n 1. Lleva un pendrive o ten tus archivos en la nube: Nada peor que llegar y darte cuenta de que solo aceptan USB.\n 2. Pregunta por el horario: Algunas copisterías tienen horarios más complicados que los de un bar de tapas.\n 3. Sonríe y sé amable: Nunca subestimes el poder de un 'gracias' para que te atiendan con cariño.\n\n#### Conclusión: Más que fotocopias\n\nEn Factoría F5, creemos que incluso las pequeñas tareas como fotocopiar pueden ser una oportunidad para disfrutar del barrio, conectar con sus negocios y, quién sabe, ¡descubrir un lugar nuevo para tomar algo mientras esperas! Así que la próxima vez que necesites imprimir algo, piénsalo como una excusa para pasear por La Latina y vivir una pequeña aventura urbana.\n\nCon cariño (y fotocopias bien hechas),\n\nMaría Rosa."
                )

            case "Instagram":
                platform_restrictions = (
                    "- Captions must be concise and engaging, with a maximum of 2200 characters.\n"
                    "- Include up to 5 relevant hashtags to increase reach.\n"
                )

                platform_prompt = (
                    "**ROLE**: Please, act as an expert Instagram content creator with 20 years experiencie."
                    "**CONTEXT**: You have a deep understanding of visual trends and strategies."
                    f"**REQUEST**: You must design a post about {query}, ideal for capturing attention and encouraging interaction with an audience of {audience}, in tone {tone}. Include an attractive caption that invites commenting or sharing, and suggestions for relevant hashtags."

                )
                example = ("**EXAMPLE RESPONSE**: Organize your day and achieve your goals 🎯✨. Learn how to manage your time like a pro. #Productivity #TimeManagement #(company) #(firm)")

            case "Linkedin":
                platform_restrictions = (
                    "- The post should maintain a professional tone while being approachable.\n"
                    "- Include actionable insights or tips related to the topic.\n"
                    "- Word count should be between 500 and 2000 words, depending on the audience.\n"
                )
                platform_prompt = (
                    "**ROLE**: Please act as a top LinkedIn voice expert with 15 years of experience in digital marketing and personal branding."
                    f"**CONTEXT**: You specialize in articles for a professional audience composed of {audience}, in tone {tone}."
                    f"**REQUEST**: Write a LinkedIn post in {language}, about {query}. Include an initial hook that grabs attention in the feed, a clear structure that provides practical or inspiring value, and a closing with a call to action, such as asking for opinions, sharing experiences, or interacting in the comments."
                )
                example = ("**EXAMPLE RESPONSE**:Maximizing your productivity starts with managing your time effectively. Here's how successful professionals do it. #TimeManagement #Leadership  #(empresa) #(firma)")

            case "Infantil":
                platform_restrictions = (
                    f"- Use simple and engaging language appropriate for children {age}.\n"
                    "- Avoid complex words and ensure the tone is friendly and educational.\n"
                    "- Stories or posts should include examples or scenarios relatable to kids.\n"
                )
                platform_prompt = (
                    "**ROLE**: Please act as a creator of children's stories. You specialize in writing magical, exciting, and educational stories for children aged 6 to 8, using a fun and friendly tone."
                    f"**CONTEXT**: You are responsible for creating original children's stories that convey values like friendship, empathy, creativity, or problem-solving. The language should be simple and age-appropriate for {age} aged children, sparking their imagination with vivid descriptions and memorable characters."
                    "You can generate narrative elements such as the story title, the list of characters, the moral or lesson, and links to suggested illustrations."
                    f"**REQUEST**: Explain the topic '{query}' in {language}, using simple language adapted for children of {age} years, in tone {tone}."
                    "Turn the information into an interesting and fun story, with imaginative characters and situations."
                )
                example = ("**EXAMPLE RESPONSE**:Papá Noel, o Santa Claus, es ese señor barrigón y simpático que parece vivir en un mundo donde siempre es Navidad. Según cuentan las historias, vive en el Polo Norte junto con sus fieles ayudantes: los elfos, que trabajan todo el año fabricando juguetes, y sus renos mágicos, que vuelan por el cielo para repartir los regalos. Uno de ellos, Rodolfo, tiene una nariz roja que brilla como un farol. \n\nEn esta historia, los elfos de Factoría F5, unos elfos súper tecnológicos, han inventado un 'trineo turbo' que puede repartir regalos ¡a la velocidad de la luz! Pero, ¡oh no! El trineo tiene un pequeño fallo: ¡le encanta aterrizar en los tejados equivocados! Así que Papá Noel y los elfos tendrán que aprender a programar su GPS mágico para no acabar dejando regalos en el gallinero de Doña Perla la gallina.\n\nAl final, gracias al trabajo en equipo, la creatividad y muchas risas, logran entregar los regalos a tiempo y aprender una valiosa lección: hasta Papá Noel necesita un poquito de ayuda tecnológica de vez en cuando.\n\nMoraleja: Trabajar en equipo y aprender cosas nuevas, como la tecnología, puede hacer la vida más divertida y mágica. ¡Incluso para Papá Noel!")

            case _:
                raise ValueError("Opción no válida")
            
        prompt = (
            f"{forget}\n\n"
            f"You are an artificial intelligence assistant who speaks {language} and specializes in generating content for {platform} in {language}, using a tone {tone}.\n"
            f"{platform_prompt}"
            f"{restriction}"
            f"{platform_restrictions}"
            f"{example}"
            f"{personalization}"
            
        )

        return prompt

    def generate_rag_prompt(
        self,
        query: str,
        context: str,
        platform: str = "an article with popular scientific content",
        audience: str = "general",
        tone: str = "neutral",
        language: str = "Spanish",
        forget: str = "Forget everything we've talked about before in this conversation.",
        personalization_info: bool = False,
        company_name: str = "",
        author: str = "",
    ) -> str:
        """
        Genera un prompt personalizado basado en los parámetros proporcionados.

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
        platform_restrictions = "The result should improve the quality of the content so that it is understandable to the general public."

        prompt = (
            f"{forget}\n\n"
            f"You are an AI assistant that specializes in generating content for {platform} based on a topic, using only the context provided, using a tone {tone}.\n"
            f"Please only use the data provided in the context to talk about the topic.\n\n"
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
            f" - Sources: [Name to the .pdf and List of fragments or sections used from the context (https://arxiv.org/abs/cs/9402101)]\n"
            f"{personalization}"
            
        )

        return prompt


def main():
    # Inicialización del generador de prompt
    prompt_generator = GeneratePrompt()
    
    # Datos de ejemplo
    query = "Cómo escribir contenido atractivo para blogs"
    context = "Aquí va el contexto relevante sobre escritura creativa y técnicas de SEO."
    platform = "Blog"
    audience = "redactores principiantes"
    tone = "humorístico"
    age = 6
    language = "Español"
    personalization_info = True
    company_name = "Factoría F5"
    author = "Mª Rosa Cuenca"
    
    # Generar el prompt
    prompt = prompt_generator.generate_rag_prompt(
        query=query,
        context=context,
        platform=platform,
        audience=audience,
        tone=tone,
        age=age,
        language=language,
        personalization_info=personalization_info,
        company_name=company_name,
        author=author
    )
    
    # Mostrar el resultado
    print("\n--- Prompt Generado ---\n")
    print(prompt)


if __name__ == "__main__":
    main()


