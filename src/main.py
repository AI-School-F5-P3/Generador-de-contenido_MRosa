from rag_pipeline import RAGPipeline
from arxiv_client import ArxivClient
from generate_prompt import GeneratePrompt
from src.utils import BRIGHT_GREEN, PASTEL_YELLOW, RESET, STAR, THINKING, CELEBRATION


def main():
    # Configuración del pipeline
    pipeline = RAGPipeline(
        embedding_model_name="sentence-transformers/all-mpnet-base-v2",
        llm_model_name="llama3-8b-8192",
        device="cpu"  # Cambiar a "cuda" si hay GPU disponible
    )

    # Definir la categoría y el término de búsqueda
    category = "math.AC"
    term = "Differential Geometry"

    # Consultar la API de arXiv
    print(f"\n{BRIGHT_GREEN}{THINKING} Consultando la API de arXiv...{RESET}")
    papers = ArxivClient.fetch_arxiv_papers(term=term, category=category, max_results=10)


    print(f"\n{BRIGHT_GREEN}{THINKING} Convirtiendo artículos a documentos...{RESET}")
    documents = ArxivClient.papers_to_documents(papers)

    print(f"\n{BRIGHT_GREEN}{THINKING} Agregando documentos al índice...{RESET}")
    pipeline.add_documents(documents)

    # Realizar una consulta
    print(f"\n{BRIGHT_GREEN}{THINKING} Realizando consulta...{RESET}")

    relevant_chunks = pipeline.retrieve_relevant_chunks(term, top_k=5)

    print(f"\n{BRIGHT_GREEN}{THINKING} Generando respuesta...{RESET}")

    # Pasar el prompt generado a `generate_response`
    response = pipeline.generate_response(term, relevant_chunks)


    response_img = pipeline.generate_image_prompt(term, relevant_chunks)

    # generador = GeneradorImagenesSD()
    # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # archivo_salida = f"assets/output_images/img_{timestamp}.png"

    # generador.generar_imagen(
    #     texto=response_img,
    #     archivo_salida=archivo_salida,
    #     alto=768,
    #     ancho=768,
    #     guidance_scale=7.5,
    #     num_steps=50,
    #     semilla=1175181494,
    #     negative_prompt="nrealfixer, nfixer, 3d render, cgi, painting, drawing, cartoon, anime,easynegative, (low quality, worst quality:1.4), bad anatomy, bad composition, out of frame, duplicate, watermark, signature, text"
    # )


    print(f"\n{BRIGHT_GREEN}{STAR} Respuesta generada {STAR} {RESET}\n")

    print(f"{PASTEL_YELLOW}{response}{RESET}")

    print(f"\n{BRIGHT_GREEN}{STAR} Prompt de imagen {STAR} {RESET}\n")

    print(f"{PASTEL_YELLOW}{response_img}{RESET}")

    print(f"\n{BRIGHT_GREEN}\nListo! {CELEBRATION}{RESET}\n")
if __name__ == "__main__":
    main()
