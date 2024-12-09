import requests
import feedparser
from langchain_core.documents import Document

class ArxivClient:
    BASE_URL = "http://export.arxiv.org/api/query"

    @staticmethod
    def fetch_arxiv_papers(category,term, max_results=5):
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
                "link": entry.link,
            })
        return papers

    @staticmethod
    def papers_to_documents(papers):
        """
        Convierte una lista de artículos en documentos para FAISS.
        """
        documents = []
        for paper in papers:
            documents.append(Document(
                page_content=paper['summary'],
                metadata={
                    "title": paper['title'],
                    "authors": paper['authors'],
                    "published": paper['published'],
                    "link": paper['link']
                }
            ))
        return documents
