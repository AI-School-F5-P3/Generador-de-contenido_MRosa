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
API_RAG_URL = os.getenv('API_RAG_URL')

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

def render_input_form(tab_key):
    """
    Renderiza el formulario de entrada con una clave única para cada pestaña.
    """
    query = st.text_input("Tema", placeholder="Introduce el tema aquí...", key=f"{tab_key}_query")
    audience = st.text_input("Audiencia", placeholder="Introduce la audiencia objetivo...", key=f"{tab_key}_audience")
    
    if tab_key == "tab2":
        col2, col3, col4, col1 = st.columns(4)
    else:
        col1, col2, col3, col4 = st.columns(4)

    with col1:
        platform = "an article with popular scientific content"
        if tab_key != "tab2":
            platform = st.selectbox(
                "Platform", 
                ["Blog", "Instagram", "Linkedin", "Infantil"], 
                key=f"{tab_key}_platform"
            )
    with col2:
        tone = st.selectbox(
            "Tono", 
            [
                "Formal", "Informal", "Objetivo", "Subjetivo", "Humorístico", "Sarcástico", 
                "Persuasivo", "Optimista", "Pesimista", "Educativo", "Autoritario",  
                "Inspirador", "Crítico", "Dramático", "Técnico", "Poético"
            ],
            key=f"{tab_key}_tone"
        )
    with col3:
        language = st.selectbox(
            "Idioma", 
            ["Español", "Inglés", "Francés", "Alemán", "Italiano", "Árabe", "Portugués", "Coreano", "Hindi"], 
            key=f"{tab_key}_language"
        )
    with col4:
        age = st.slider(
            "Edad", 3, 12, value=6, key=f"{tab_key}_age"
        ) if platform == "Infantil" else None


    col_personalization, col_img = st.columns([1, 3])
    
    with col_personalization:
        personalization_info = st.checkbox("Personalizar", key=f"{tab_key}_personalization_info")
    with col_img:
        ai_image = st.checkbox("Imagen", key=f"{tab_key}_ai_image")
    
    # Variables de personalización
    company_name, author = "", ""
    if personalization_info:
        company_name = st.text_input("Nombre de la empresa", placeholder="Empresa...", key=f"{tab_key}_company_name")
        author = st.text_input("Nombre del/a autor/a", placeholder="Autor/a...", key=f"{tab_key}_author")
    
    return {
        "query": query,
        "audience": audience,
        "platform": platform,
        "tone": tone,
        "language": language,
        "age": age if age else None,
        "personalization_info": personalization_info,
        "company_name": company_name,
        "author": author,
        "ai_image": ai_image,
    }

# Crear pestañas
tab1, tab2 = st.tabs(["Redes sociales", "Artículo científico"])

with tab1:

    tab1_col1, tab1_col2 = st.columns([1.5, 1])  # La primera columna es 1.5 veces más ancha que la segunda

    with tab1_col1:
        tab1_inputs = render_input_form("tab1") 
        # Botón para generar contenido
        generate_button = st.button("Generar Contenido", key="generate_button_tab1")

    with tab1_col2:
        with st.container(key="svgimage_tab1"):
            svg_write()

    if generate_button:            
        query = tab1_inputs["query"]
        audience = tab1_inputs["audience"]
        platform = tab1_inputs["platform"]
        tone = tab1_inputs["tone"]
        language = tab1_inputs["language"]
        age = tab1_inputs["age"]
        personalization_info = tab1_inputs["personalization_info"]
        company_name = tab1_inputs["company_name"]
        author = tab1_inputs["author"]
        ai_image = tab1_inputs["ai_image"]

        if query.strip() == "":
            st.error("El campo Tema es obligatorio. Por favor, ingrese un valor.")
        elif audience.strip() == "":
            st.error("El campo Audiencia es obligatorio. Por favor, ingrese un valor.")
        elif personalization_info == True:
            if (company_name.strip() == "") and (author.strip() == ""):
                st.error("Debe introducir al menos Empresa o Autor.")
        else:
            with st.spinner("Generando contenido..."):
                # Crear el payload para la solicitud
                payload = {
                    "query": query,
                    "platform": platform,
                    "audience": audience,
                    "tone": tone,
                    "age": age if age is not None and age > 0 else None,
                    "language": language,
                    "personalization_info": personalization_info,
                    "company_name": company_name,
                    "author": author,
                }
                
                try:
                    # Enviar la solicitud al backend
                    response = requests.post(API_URL, json=payload)

                    # Intentar obtener el JSON de la respuesta
                    if response.status_code == 200:
                            data = response.json()
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
                            print(f"❌ {response.status_code}: {response.text}")
                            st.error(f"Error del servidor ({response.status_code}): {response.text}")
                except requests.RequestException as e:
                        st.error(f"Error al conectar con el servidor: {e}")



with tab2:
    tab2_col1, tab2_col2 = st.columns([1.5, 1])  # La primera columna es 1.5 veces más ancha que la segunda

    with tab2_col1:
        selected_category = st.selectbox("Selecciona una categoría principal", categories.keys())
        if selected_category:
            subcategories = categories[selected_category]
            selected_subcategory = st.selectbox("Selecciona una subcategoría", subcategories.keys())

            if selected_subcategory:
                category = subcategories[selected_subcategory]
                st.write(f"Has seleccionado: {selected_category} → {subcategories[selected_subcategory]}")

        tab2_inputs = render_input_form("tab2") 

        # Botón para generar contenido
        generate_rag_button = st.button("Generar Contenido", key="generate_button_tab2")

    with tab2_col2:
        with st.container(key="svgimage_tab2"):
            svg_write()

    if generate_rag_button:
        query = tab2_inputs["query"]
        audience = tab2_inputs["audience"]
        platform = tab2_inputs["platform"]
        tone = tab2_inputs["tone"]
        language = tab2_inputs["language"]
        age = tab2_inputs["age"]
        personalization_info = tab2_inputs["personalization_info"]
        company_name = tab2_inputs["company_name"]
        author = tab2_inputs["author"]
        ai_image = tab2_inputs["ai_image"]

        if query.strip() == "":
            st.error("El campo Tema es obligatorio. Por favor, ingrese un valor.")
        elif audience.strip() == "":
            st.error("El campo Audiencia es obligatorio. Por favor, ingrese un valor.")
        elif personalization_info == True:
            if (company_name.strip() == "") and (author.strip() == ""):
                st.error("Debe introducir al menos Empresa o Autor.")
        else:
            with st.spinner("Generando contenido..."):
                # Crear el payload para la solicitud
                payload = {
                    "query": query,
                    "category": category,
                    "platform": platform,
                    "audience": audience,
                    "tone": tone,
                    "age": age if age is not None and age > 0 else None,
                    "language": language,
                    "personalization_info": personalization_info,
                    "company_name": company_name,
                    "author": author,
                }
                
                try:
                    # Enviar la solicitud al backend
                    response = requests.post(API_RAG_URL, json=payload)

                    # Intentar obtener el JSON de la respuesta
                    if response.status_code == 200:
                            data = response.json()
                            # Mostrar un mensaje con HTML
                            st.header("Disfruta de tu contenido")
                            with st.container(key="rag"):                                  
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
                            print(f"❌ {response.status_code}: {response.text}")
                            st.error(f"Error del servidor ({response.status_code}): {response.text}")
                except requests.RequestException as e:
                        st.error(f"Error al conectar con el servidor: {e}")