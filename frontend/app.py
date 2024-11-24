import streamlit as st
import requests
import json

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
                # Convertir el texto JSON anidado en un diccionario
                try:
                    data = json.loads(response_data["respuesta"])  # Si "respuesta" es un JSON en formato de cadena
                except json.JSONDecodeError:
                    st.error(f"La respuesta no tiene un formato JSON válido. \n{response_data["respuesta"]}")
                    data = None

                if data:
                    # Acceder a los valores del diccionario
                    texto = data.get("txt", "Texto no disponible.")
                    descripcion_imagen = data.get("img", "Descripción de imagen no disponible.")

                    # Mostrar los resultados
                    st.success(f"{texto}")
                    st.info(f"{descripcion_imagen}")

            else:
                st.error("La respuesta no contiene la clave 'respuesta'.")
        else:
            # Manejar errores del servidor
            st.error(f"Error del servidor ({response.status_code}): {response.text}")

    except requests.RequestException as e:
        # Manejar errores de conexión
        st.error(f"Error al conectar con el servidor: {e}")
