import streamlit as st
import requests
import json

import re
import json

def sanitize_to_json(text):
    """
    Limpia y corrige un texto para que sea un JSON válido.
    """
    try:
        # Intenta cargar directamente como JSON
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            # Reemplazar comillas simples por dobles
            sanitized_text = text.replace("'", '"')

            # Escapar caracteres especiales comunes (\n, \t, etc.)
            sanitized_text = sanitized_text.replace("\n", "\\n").replace("\t", "\\t")

            # Agregar comillas dobles a claves JSON no entrecomilladas
            sanitized_text = re.sub(r'(?<!")(\b[a-zA-Z_][a-zA-Z0-9_]*\b)(?=\s*:)', r'"\1"', sanitized_text)

            # Validar y cargar el JSON
            return json.loads(sanitized_text)
        except Exception as e:
            # Si aún falla, devolver un error detallado
            raise ValueError(f"Error al sanitizar el texto: {e}\nTexto problemático:\n{text}")

# URL del backend de FastAPI
API_URL = "http://127.0.0.1:8000/generar"

# Título de la aplicación
st.title("Generador de Contenido Automatizado")

# Formulario para la entrada del usuario
plataforma = st.selectbox("Plataforma", ["blog", "twitter", "instagram", "SEO", "infantil"])
tema = st.text_input("Tema", placeholder="Introduce el tema aquí...")
audiencia = st.text_input("Audiencia", placeholder="Introduce la audiencia objetivo...")
tono = st.selectbox(
    "Tono", 
    [
        "formal", "informal", "objetivo", "subjetivo", "humorístico", "sarcástico", 
        "persuasivo", "optimista", "pesimista", "apasionado", "nostálgico", 
        "respetuoso", "educativo", "autoritario", "entusiasta", "melancólico", 
        "inspirador", "crítico", "descriptivo", "reflexivo", "sincero", "dramático", 
        "técnico", "empático", "cínico", "formal-poético"
    ]
)
edad = st.slider("Edad (solo para infantil)", 3, 12, value=6) if plataforma == "infantil" else None

# Botón para generar contenido
if st.button("Generar Contenido"):
    # Crear el payload para la solicitud
    payload = {
        "plataforma": plataforma,
        "tema": tema,
        "audiencia": audiencia,
        "tono": tono,
        "edad": edad
    }

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
                    # Acceder a los valores del diccionario
                    texto = data.get("txt", "Texto no disponible.")
                    descripcion_imagen = data.get("img", "Descripción de imagen no disponible.")

                    # Mostrar los resultados
                    st.success(f"{texto}")
                    st.info(f"{descripcion_imagen}")
                else:
                    st.error("No se pudo convertir la respuesta a un JSON válido.")
            else:
                st.error("La respuesta no contiene la clave 'respuesta'.")
        else:
            # Manejar errores del servidor
            st.error(f"Error del servidor ({response.status_code}): {response.text}")

    except requests.RequestException as e:
        # Manejar errores de conexión
        st.error(f"Error al conectar con el servidor: {e}")
