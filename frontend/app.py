import streamlit as st
import requests
import json
import re
import os
from dotenv import main
from src.text_to_image import GeneradorImagenesSD
import datetime
from src.utils import local_css, svg_write

# Cargar variables de entorno
main.load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Acceder a las variables de entorno
API_URL = os.getenv('API_URL')

# Cargar configuración y CSS
local_css(os.path.join(os.path.dirname(__file__), 'static', 'style.css'))
local_css(os.path.join(os.path.dirname(__file__), 'static', 'creativity-styles.css'))

# Título de la aplicación
st.image("./frontend/static/img/logo.png", width = 300)

# Diccionario de categorías para la pestaña    
categories = {
    "Computer Science": {
        "Inteligencia Artificial": "cs.AI",
        "Arquitectura de Hardware": "cs.AR",
        "Complejidad Computacional": "cs.CC",
        "Ingeniería Computacional, Finanzas y Ciencias": "cs.CE",
        "Geometría Computacional": "cs.CG",
        "Computación y Lenguaje": "cs.CL",
        "Criptografía y Seguridad": "cs.CR",
        "Visión por Computador y Reconocimiento de Patrones": "cs.CV",
        "Computadoras y Sociedad": "cs.CY",
        "Bases de Datos": "cs.DB",
        "Computación Distribuida, Paralela y en Clústeres": "cs.DC",
        "Bibliotecas Digitales": "cs.DL",
        "Matemáticas Discretas": "cs.DM",
        "Estructuras de Datos y Algoritmos": "cs.DS",
        "Tecnologías Emergentes": "cs.ET",
        "Lenguajes Formales y Teoría de Autómatas": "cs.FL",
        "Literatura General": "cs.GL",
        "Gráficos": "cs.GR",
        "Ciencias de la Computación y Teoría de Juegos": "cs.GT",
        "Interacción Humano-Computadora": "cs.HC",
        "Recuperación de Información": "cs.IR",
        "Teoría de la Información": "cs.IT",
        "Aprendizaje Automático": "cs.LG",
        "Lógica en Ciencias de la Computación": "cs.LO",
        "Sistemas Multiagente": "cs.MA",
        "Multimedia": "cs.MM",
        "Software Matemático": "cs.MS",
        "Análisis Numérico": "cs.NA",
        "Computación Neural y Evolutiva": "cs.NE",
        "Redes y Arquitectura de Internet": "cs.NI",
        "Otras Ciencias de la Computación": "cs.OH",
        "Sistemas Operativos": "cs.OS",
        "Rendimiento": "cs.PF",
        "Lenguajes de Programación": "cs.PL",
        "Robótica": "cs.RO",
        "Cálculo Simbólico": "cs.SC",
        "Sonido": "cs.SD",
        "Ingeniería de Software": "cs.SE",
        "Redes Sociales e Información": "cs.SI",
        "Sistemas y Control": "cs.SY",
    },
    "Economía":{
        "Econometría": "econ.EM",
        "Economía General": "econ.GN",
        "Economía Teórica": "econ.TH",
    },
    "Ingeniería Eléctrica y Ciencias de los Sistemas": {
        "Procesamiento de Audio y Voz": "eess.AS",
        "Procesamiento de Imágenes y Videos": "eess.IV",
        "Procesamiento de Señales": "eess.SP",
    },
    "Matemáticas": {
        "Álgebra Conmutativa": "math.AC",
        "Geometría Algebraica": "math.AG",
        "Análisis de EDPs (Ecuaciones en Derivadas Parciales)": "math.AP",
    },
}

# Crear pestañas
# tab1, tab2 = st.tabs(["Principal", "Categorías"])

# with tab1:
    # Título de la aplicación

col1, col2 = st.columns([1.5, 1])  # La primera columna es 1.5 veces más ancha que la segunda

with col1:
        
        # Formulario para la entrada del usuario
        selected_category = st.selectbox("Selecciona una categoría principal", categories.keys())
        if selected_category:
            subcategories = categories[selected_category]
            selected_subcategory = st.selectbox("Selecciona una subcategoría", subcategories.keys())

            if selected_subcategory:
                category = subcategories[selected_subcategory]
                # st.write(f"Has seleccionado: {selected_category} → {subcategories[selected_subcategory]}")
        query  = st.text_input("Tema", placeholder="Introduce el tema aquí...")
        audience = st.text_input("Audiencia", placeholder="Introduce la audiencia objetivo...")
        col11, col12, col13, col14  = st.columns(4)        
        with col11:
            platform = st.selectbox("platform", ["Blog", "Twitter", "Instagram", "Linkedin", "Infantil"])
        with col12:
            tone = st.selectbox(
            "Tono", 
            [
                "Formal", "Informal", "Objetivo", "Subjetivo", "Humorístico", "Sarcástico", 
                "Persuasivo", "Optimista", "Pesimista", "Educativo", "Autoritario",  
                "Inspirador", "Crítico", "Dramático", "Técnico", "Poético"
            ]
        )
        with col13:
            language = st.selectbox(
                "Idioma", 
                ["Español", "Inglés", "Francés", "Alemán", "Italiano", "Árabe", "Portugués", "Coreano", "Hindi"]
            )
        with col14:
            age = st.slider("Edad", 3, 12, value=6) if platform == "Infantil" else None

        col_personalization, col_img  = st.columns([1, 3])   

        with col_personalization:
            # Personalización
            personalization_info = st.checkbox("Personalizar")
        with col_img:

            # Imagen
            ai_image = st.checkbox("Imagen")

        # Inicializar variables de personalización
        company_name = ""
        author = ""

        if personalization_info:
            company_name = st.text_input("Nombre de la empresa", placeholder="Empresa...")
            author = st.text_input("Nombre del/a autor/a", placeholder="Autor/a...")
        else:
            company_name = ""
            author = ""

with col2:
    with st.container(key="svgimage"):
        svg_write()

# Botón para generar contenido
if st.button("Generar Contenido"):
        if query.strip() == "":
                st.error("El campo Tema es obligatorio. Por favor, ingrese un valor.")
        elif audience.strip() == "":
                st.error("El campo Audiencia es obligatorio. Por favor, ingrese un valor.")
        elif personalization_info == True:
            if (company_name.strip() == "") and (author.strip() == ""):
                st.error("Debe introducir al menos Empresa o Autor.")
        else:
            with st.spinner("Generando contenido..."):
                print("GENERANDO CONTENIDO...")
                # Crear el payload para la solicitud
                payload = {
                    "query": query,
                    "category": category,
                    "platform": platform,
                    "audience": audience,
                    "tone": tone,
                    "age": age if age and age > 0 else None,
                    "language": language,
                    "personalization_info": personalization_info,
                    "company_name": company_name,
                    "author": author,
                }
                print(f"PAYLOAD... {payload}")
                try:
                    # Enviar la solicitud al backend
                    response = requests.post(API_URL, json=payload)
                    
                    
                    # Intentar obtener el JSON de la respuesta
                    if response.status_code == 200:
                        data = response.json()
                        print(f"response_data... {data}")
                        # Mostrar un mensaje con HTML
                        st.header("Disfruta de tu contenido")
                        with st.container(key="lolo"):                                  
                            # Acceder a los valores del diccionario
                            texto = data.get("txt", "Texto no disponible.")
                            descripcion_imagen = data.get("img", "Descripción de imagen no disponible.")
                            col1, col2  = st.columns([1.5, 1])       
                            with col1:                       
                                # Mostrar el texto con un spinner
                                with st.spinner("Generando texto..."):
                                    st.write(f"{texto}")
                            with col2:
                                # Generar la imagen con un spinner
                                with st.spinner("Generando imagen..."):
                                                
                                    # Generar imagen si está el check activado
                                    if ai_image:
                                        
                                        generador = GeneradorImagenesSD()
                                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                                        archivo_salida = f"assets/output_images/img_{timestamp}.png"
                                        # Generar imagen comentado
                                        generador.generar_imagen(
                                            texto=descripcion_imagen,
                                            archivo_salida=archivo_salida,
                                            alto=512,
                                            ancho=512,
                                            guidance_scale=7.5,
                                            num_steps=10,
                                            semilla=1175181494,
                                            negative_prompt="nrealfixer, nfixer, 3d render, cgi, painting, drawing, cartoon, anime,easynegative, (low quality, worst quality:1.4), bad anatomy, bad composition, out of frame, duplicate, watermark, signature, text"
                                        )
                                        st.image(archivo_salida, caption=descripcion_imagen, use_container_width=True)
                    elif response.status_code == 400:
                        error_response = response.json()
                        if (tone == "Humorístico") or (tone == "Sarcástico"):
                            st.error("❌ Te voy a lavar la boca con lejía")
                        else:
                            st.error(f"❌ {json.loads(response.text)['detail']}")
                    else:
                        print(f"❌❌❌❌❌❌❌❌❌... {response.status_code}: {response.text}")
                        st.error(f"Error del servidor ({response.status_code}): {response.text}")
                except requests.RequestException as e:
                    st.error(f"Error al conectar con el servidor: {e}")

# with tab2:
    # col1, col2 = st.columns([1.5, 1])  # La primera columna es 1.5 veces más ancha que la segunda

    # with col1:
    #     st.write("hola")
    #     # selected_category = st.selectbox("Selecciona una categoría principal", categories.keys())

    #     # if selected_category:
    #     #     subcategories = categories[selected_category]
    #     #     selected_subcategory = st.selectbox("Selecciona una subcategoría", subcategories.keys())

    #     #     if selected_subcategory:
    #     #         st.write(f"Has seleccionado: {selected_category} → {subcategories[selected_subcategory]}")

    # with col2:
    #     with st.container(key="svgimage_t2"):
    #         svg_write()

    # # Botón para generar contenido
    # if st.button("Generar Contenido", key='boton2'):
        
    #             # Crear el payload para la solicitud
    #             payload = {
    #                 "platform": "Blog",
    #                 "topic": "I don't know what to write",
    #                 "audience": "general",
    #                 "tone": "neutral",
    #                 "age": 0,
    #                 "language": "Spanish",
    #                 "forget": "Forget everything we've talked about before in this conversation.",
    #                 "output_format": "",
    #                 "restriction": "",
    #                 "personalization_info": False,
    #                 "company_name": "",
    #                 "author": ""
    #             }
    #             print(f"PAYLOAD... {payload}")
    #             try:
    #                 # Enviar la solicitud al backend
    #                 response = requests.post(API_RAG, json=payload)
    #                 print(f"PAYLOAD... {response}")
                    
    #                 # Intentar obtener el JSON de la respuesta
    #                 if response.status_code == 200:
    #                     response_data = response.json()

    #                     # Mostrar un mensaje con HTML
    #                     st.header("Disfruta de tu contenido")
    #                     with st.container(key="lolo"):                                  
    #                         # Acceder a los valores del diccionario
    #                         texto = data.get("txt", "Texto no disponible.")
    #                         descripcion_imagen = data.get("img", "Descripción de imagen no disponible.")
    #                         col1, col2  = st.columns([1.5, 1])       
                                                                       
  
    #                 elif response.status_code == 400:
    #                     error_response = response.json()
    #                     if (tone == "Humorístico") or (tone == "Sarcástico"):
    #                         st.error("❌ Te voy a lavar la boca con lejía")
    #                     else:
    #                         st.error(f"❌ {json.loads(response.text)['detail']}")
    #                 else:
    #                     print(f"❌❌❌❌❌❌❌❌❌... {response.status_code}: {response.text}")
    #                     st.error(f"Error del servidor ({response.status_code}): {response.text}")
    #             except requests.RequestException as e:
    #                 st.error(f"Error al conectar con el servidor: {e}")
