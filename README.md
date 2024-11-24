# Generador-de-contenido_MRosa
Generador de contenido - María Rosa


    Generador-de-contenido/
    │
    ├── api/                         # Backend con FastAPI
    │   ├── __init__.py
    │   ├── main.py                  # Punto de entrada de la API
    │   └── routers/                 # (Opcional) Archivos de rutas para organizar endpoints
    │
    ├── frontend/                    # Aplicación de Streamlit
    │   ├── __init__.py
    │   ├── app.py                   # Punto de entrada de Streamlit
    │
    ├── src/                         # Lógica del negocio y componentes compartidos
    │   ├── __init__.py
    │   ├── moderation.py            # Moderación de contenido
    │   ├── model_client.py          # Cliente para interactuar con el modelo
    │   ├── prompt_manager.py        # Gestión de prompts y validaciones
    │
    └── requirements.txt             # Dependencias del proyecto
