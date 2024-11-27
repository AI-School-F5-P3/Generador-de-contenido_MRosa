import streamlit as st
import json
import re

def sanitize_to_json(text):
    """
    Limpia y corrige un texto para que sea un JSON válido.
    """
    try:
        # Intenta cargar directamente como JSON
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            print(f'\n\n======================================== TEXTO ORIGINAL SIN SANEAR ==============================\n\n{text}\n\n=================================================================================================')
            # Reemplazar comillas simples por dobles
            sanitized_text = text.replace("'", '"')

            # Combinar hashtags huérfanos con el contenido de 'txt'
            sanitized_text = sanitized_text.replace('","#', ' #')

            # Escapar caracteres de control no escapados (\n, \r, \t)
            sanitized_text = re.sub(r'(?<!\\)([\n\r\t])', lambda match: f'\\{match.group(1)}', sanitized_text)

            # Validar y cargar el JSON corregido
            try:
                return json.loads(sanitized_text)
            except json.JSONDecodeError:
                # Si no es un JSON, devolver una estructura predeterminada
                return {"txt": sanitized_text.replace('txt:', ''), "img": ""}

        except Exception as nested_e:
            raise ValueError(f"Error al sanear el texto: {nested_e}\nTexto problemático:\n{text}")


def add_personalization(content, personalization_info):
    """
    Agrega personalización al contenido generado.

    Parameters:
        content (dict): Contenido generado como un diccionario JSON.
        personalization_info (dict): Información de personalización con las claves:
            - 'company_name': Nombre de la empresa.
            - 'author': Autor del contenido.

    Returns:
        dict: Contenido con la personalización añadida.
    """
    if personalization_info:
        personalization_prompt = (
            f"Esta publicación es presentada por {personalization_info.get('company_name', 'una empresa anónima')}. "
            f"Autor: {personalization_info.get('author', 'Desconocido')}. "
        )

        # Modificar el campo 'txt' del contenido
        if "txt" in content:
            content["txt"] = personalization_prompt + content["txt"]

        # Añadir contexto personalizado al prompt de la imagen si existe
        if "img" in content and content["img"]:
            content["img"] = (
                f"Contextualizado para {personalization_info.get('company_name', 'una company_name')}: "
                + content["img"]
            )

    return content


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'''
                <head>
                    <!-- Material Icons -->
                    <link href="{url}" rel="stylesheet">
                </head>
                ''', unsafe_allow_html=True)   