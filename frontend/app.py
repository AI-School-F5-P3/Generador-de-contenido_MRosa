import streamlit as st
import requests
import json
import re
import os
from dotenv import main
from src.text_to_image import GeneradorImagenesSD
import datetime
from frontend.utils import local_css, sanitize_to_json, svg_write

# Cargar variables de entorno
main.load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Acceder a las variables de entorno
API_URL = os.getenv('API_URL')

# Cargar configuración y CSS
local_css(os.path.join(os.path.dirname(__file__), 'static', 'style.css'))
local_css(os.path.join(os.path.dirname(__file__), 'static', 'creativity-styles.css'))

# Título de la aplicación


col1, col2 = st.columns([1.5, 1])  # La primera columna es 1.5 veces más ancha que la segunda

with col1:
    st.title("Generador de Contenido")
    # Formulario para la entrada del usuario
    topic = st.text_input("Tema", placeholder="Introduce el topic aquí...")
    audience = st.text_input("Audiencia", placeholder="Introduce la audience objetivo...")
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
        age = st.slider("Edad (solo para infantil)", 3, 12, value=6) if platform == "Infantil" else None
    # Información de personalización
    personalization_info = st.checkbox("Personalizar")

    # Inicializar variables de personalización
    company_name = None
    author = None

    if personalization_info:
        company_name = st.text_input("Nombre de la empresa", placeholder="Empresa...")
        author = st.text_input("Nombre del/a autor/a", placeholder="Autor/a...")

with col2:
    svg_write()








# Botón para generar contenido
if st.button("Generar Contenido"):
    if topic.strip() == "":
            st.error("El campo de topic es obligatorio. Por favor, ingrese un valor.")
    elif audience.strip() == "":
            st.error("El campo de audience es obligatorio. Por favor, ingrese un valor.")
    elif personalization_info == True:
        if (company_name.strip() == "") and (author.strip() == ""):
            st.error("Debe introducir al menos Empresa o Autor.")
        else:
            with st.spinner("Generando contenido..."):
                # Crear el payload para la solicitud
                payload = {
                    "platform": platform,
                    "topic": topic,
                    "audience": audience,
                    "tone": tone,
                    "age": age,
                    "language": language,
                    "personalization_info": personalization_info,
                    "company_name": company_name,
                    "author": author,
                }
                # st.write(payload)
                try:
                    # Enviar la solicitud al backend
                    response = requests.post(API_URL, json=payload)
                    
                    # Intentar obtener el JSON de la respuesta
                    if response.status_code == 200:
                        response_data = response.json()
                        # Validar si "respuesta" está presente
                        if "respuesta" in response_data:
                            # Intentar sanitizar y cargar el JSON de la respuesta
                            data = sanitize_to_json(response_data["respuesta"])
                            if data:
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
                                    
                            else:
                                st.error(response_data["respuesta"])
                        else:
                            st.error("La respuesta no contiene la clave 'respuesta'.")
                    elif response.status_code == 400:
                        error_response = response.json()
                        if (tone == "humorístico") or (tone == "sarcástico"):
                            st.error("❌ Te voy a lavar la boca con lejía")
                        else:
                            print(f"\n\n=================================================\n\nContenido de response.text:\n\n{response.text}\n\n=================================================")
                            st.error(f"❌ {json.loads(response.text)['detail']}")
                    else:
                        st.error(f"Error del servidor ({response.status_code}): {response.text}")

                except requests.RequestException as e:
                    st.error(f"Error al conectar con el servidor: {e}")
