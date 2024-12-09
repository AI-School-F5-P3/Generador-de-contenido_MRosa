from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from src.rag_pipeline import RAGPipeline 
from src.arxiv_client import ArxivClient
from src.moderation import Moderation

# Inicializa FastAPI
app = FastAPI()

# Modelo para los parámetros de entrada
class QueryParams(BaseModel):
    query: str
    category: str
    platform: str = "Blog"
    audience: str = "general"
    tone: str = "neutral"
    age: Optional[int] = None
    language: str = "Spanish"
    personalization_info: bool = False
    company_name: str = ""
    author: str = ""

# Inicializa el pipeline
pipeline = RAGPipeline(
    embedding_model_name="sentence-transformers/all-mpnet-base-v2",
    llm_model_name="llama3-8b-8192",
    device="cpu"  # Cambiar a "cuda" si hay GPU disponible
)

moderation = Moderation() # Modera el texto

@app.post("/generate-response/")
def generate_response(params: QueryParams):

    score_a = moderation.moderate(params.query) 
    formatted_score_a = round(score_a * 100, 2)  # Multiplicamos por 100 y redondeamos a 2 decimales

    score_b = moderation.moderate(params.audience)    
    formatted_score_b = round(score_b * 100, 2) 

    if score_a > 0.5:
        raise HTTPException(
            status_code=400,
            detail=f"Por favor, revisa el texto para evitar lenguaje ofensivo en el tema (hate score = {formatted_score_a}%)."
        )
    elif score_b > 0.5:
        raise HTTPException(
            status_code=400,
            detail=f"Por favor, dirigete a tu audiencia con respeto (hate score = {formatted_score_b}%)."
        )


    try:
        # Crear el prompt 
        term = params.query
        category = params.category  # Ejemplo, puedes ajustar esto
        papers = ArxivClient.fetch_arxiv_papers(term=term, category=category, max_results=10)
        documents = ArxivClient.papers_to_documents(papers)
        pipeline.add_documents(documents)

        # Recupera y genera la respuesta
        relevant_chunks = pipeline.retrieve_relevant_chunks(term, top_k=5)
        response = pipeline.generate_response(term, relevant_chunks)
        response_img = pipeline.generate_image_prompt(term, relevant_chunks)

        return {
            "txt": response,
            "img": response_img
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))