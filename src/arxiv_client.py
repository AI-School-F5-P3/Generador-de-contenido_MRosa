import requests
import feedparser
import hashlib
from langchain_core.documents import Document

class ArxivClient:
    BASE_URL = "http://export.arxiv.org/api/query"

    @staticmethod
    def fetch_arxiv_papers(category, max_results=5):
        """
        Consulta la API de arXiv y devuelve una lista de artículos.
        """
        query = f"cat:{category}"
        params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
        }
        response = requests.get(ArxivClient.BASE_URL, params=params)
        feed = feedparser.parse(response.content)

        papers = []
        for entry in feed.entries:
            papers.append({
                "title": entry.title,
                "summary": entry.summary,
                "authors": [author.name for author in entry.authors],
                "published": entry.published,
                "link": entry.link,  # El enlace único
            })
        return papers

    @staticmethod
    def papers_to_documents(papers):
        """
        Convierte una lista de artículos en documentos, generando identificadores únicos basados en el enlace.
        """
        documents = []
        for paper in papers:
            # Verificar que 'link' exista y no sea None
            link = paper.get('link', 'unknown_link')

            # Generar un ID único basado en el enlace
            unique_id = hashlib.md5(link.encode('utf-8')).hexdigest()

            documents.append(Document(
                page_content=paper['summary'],
                metadata={
                    "id": unique_id,  # Identificador único basado en el enlace
                    "title": paper.get('title', 'unknown_title'),
                    "authors": paper.get('authors', []),
                    "published": paper.get('published', 'unknown_date'),
                    "link": link
                }
            ))
        return documents
