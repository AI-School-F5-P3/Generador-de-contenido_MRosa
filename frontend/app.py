import streamlit as st
import requests

# URL del backend de FastAPI
API_URL = "http://127.0.0.1:8000/generar"

# Título de la aplicación
st.title("Generador de Contenido Automatizado")

# Formulario para la entrada del usuario
plataforma = st.selectbox("Plataforma", ["blog", "twitter", "instagram", "SEO", "infantil"])
tema = st.text_input("Tema")
audiencia = st.text_input("Audiencia")
tono = st.selectbox("Tono", ["formal", "informal", "objetivo", "subjetivo", "humorístico", "sarcástico", "persuasivo", "optimista", "pesimista", "apasionado", "nostálgico", "respetuoso", "educativo", "autoritario", "entusiasta", "melancólico", "inspirador", "crítico", "descriptivo", "reflexivo", "sincero", "dramático", "técnico", "empático", "cínico", "formal-poético"])
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
        response_data = response.json()

        if response.status_code == 200:
            # Mostrar la respuesta generada
            st.success("Contenido Generado:")
            st.write(response_data["respuesta"])
        else:
            # Mostrar errores
            st.error(f"Error: {response_data['detail']}")
    except Exception as e:
        st.error(f"Error al conectar con el servidor: {e}")