import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from groq import Groq

from src.generate_prompt import GeneratePrompt

from src.utils import get_env_key,BRIGHT_GREEN,TURQUOISE,RESET,STAR, CROSS_MARK

class RAGPipeline:
    def __init__(self, embedding_model_name="sentence-transformers/all-mpnet-base-v2", llm_model_name="llama3-70b-8192", device="cpu"):
        """
        Inicializa la clase RAGPipeline con modelos de embeddings, FAISS y LLM.
        """
        # Configuración del modelo de embeddings
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs={"device": device},
            encode_kwargs={"normalize_embeddings": False}
        )
        

        try:
            key = get_env_key("GROQ_API_KEY", levels_up=1)
            if not key:
                raise ValueError(f"{BRIGHT_GREEN} La clave GROQ_API_KEY no está configurada.{RESET}")

        except FileNotFoundError as e:
            print(f'{CROSS_MARK} FileNotFoundError ------> {e}{RESET}')


        # Inicializar el cliente Groq
        self.llm_client = Groq(api_key=key)

        # Configuración de FAISS
        embedding_dim = len(self.embedding_model.embed_query("test"))
        
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.docstore = InMemoryDocstore({})
        self.index_to_docstore_id = {}

        self.vectorstore = FAISS(
            embedding_function=self.embedding_model,
            index=self.index,
            docstore=self.docstore,
            index_to_docstore_id=self.index_to_docstore_id
        )

        # Modelo de lenguaje generativo
        self.llm_client = Groq()
        self.llm_model_name = llm_model_name

        # Instanciar GeneratePrompt
        self.prompt_generator = GeneratePrompt()

    def add_documents(self, documents):
        """
        Agrega documentos al índice FAISS usando IDs únicos preexistentes en los metadatos.
        """
        print("Adding documents...")

        # Extraer los IDs de los documentos
        ids = []
        for doc in documents:
            if "id" not in doc.metadata:
                raise ValueError("Document metadata must contain an 'id' field.")
            ids.append(doc.metadata["id"])

        # Verificar si los IDs ya existen en el índice
        existing_ids = set(self.vectorstore.index_to_docstore_id.values())
        new_ids = [doc_id for doc_id in ids if doc_id not in existing_ids]

        if not new_ids:
            print("All documents already exist in the index. Skipping addition.")
            return

        # Filtrar documentos que tienen IDs únicos
        documents_to_add = [
            doc for doc in documents if doc.metadata["id"] in new_ids
        ]

        if len(documents_to_add) == 0:
            print("No new documents to add.")
            return

        # Agregar los documentos al vectorstore
        self.vectorstore.add_documents(documents=documents_to_add, ids=new_ids)
        print(f"Successfully added {len(documents_to_add)} new documents.")



    def retrieve_relevant_chunks(self, query, top_k=5):
        """
        Recupera los fragmentos más relevantes utilizando FAISS.
        """
        return self.vectorstore.similarity_search(query=query, k=top_k)
        

    def generate_response(self, query, platform, audience, tone, age, language, personalization_info, company_name, author):
        """
        Genera una respuesta basada en los fragmentos recuperados.
        """
                
        # Generar el prompt
        prompt = self.prompt_generator.generate_prompt(
            query=query,
            platform=platform,
            audience=audience,
            tone=tone,
            age=age,
            language=language,
            personalization_info=personalization_info,
            company_name=company_name,
            author=author
        )
        
        print(f"\n{BRIGHT_GREEN}{STAR} PROMPT {STAR}{RESET}")
        print(f"\n{TURQUOISE}{prompt}{RESET}\n")

        completion = self.llm_client.chat.completions.create(
            model=self.llm_model_name,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stop=None,
        )
        
        return completion.choices[0].message.content

    def generate_rag_response(self, query, context_chunks, platform, audience, tone, age, language, personalization_info, company_name, author):
        """
        Genera una respuesta basada en los fragmentos recuperados.
        """
        context = "\n".join([chunk.page_content for chunk in context_chunks])
        forget = "Forget everything we've talked about before in this conversation."

                
        # Generar el prompt
        prompt = self.prompt_generator.generate_rag_prompt(
            query=query,
            context=context,
            platform=platform,
            audience=audience,
            tone=tone,
            language=language,
            forget=forget,
            personalization_info=personalization_info,
            company_name=company_name,
            author=author
        )
        
        print(f"\n{BRIGHT_GREEN}{STAR} PROMPT {STAR}{RESET}")
        print(f"\n{TURQUOISE}{prompt}{RESET}\n")

        completion = self.llm_client.chat.completions.create(
            model=self.llm_model_name,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stop=None,
        )
        return completion.choices[0].message.content

    
    def generate_image_prompt(self, query):
        """
        Genera una respuesta basada en los fragmentos recuperados.
        """

        prompt = (
            f"You are an AI assistant specialized in generating a valid prompt for stabilityai/stable-diffusion-2-1 to illustrate this topic: {query}.\n"
"You must provide only the English prompt as a response.\n"
"Example response: Portrait of a female programmer working in an office using an AI assistant, modern office environment, bright daylight, computer and tablet screens showing AI related data and algorithms."
"You can only use a maximum of 77 tokens. Your interlocutor is the stable diffusion model, so skip phrases like 'Here is a valid prompt for stabilityai/stable-diffusion-2-1:'")     
        print(f"\n{BRIGHT_GREEN}{STAR} PROMPT {STAR}{RESET}")
        print(f"\n{TURQUOISE}{prompt}{RESET}\n")

        completion = self.llm_client.chat.completions.create(
            model=self.llm_model_name,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stop=None,
        )
        return completion.choices[0].message.content

    def generate_rag_image_prompt(self, query, context_chunks):
        """
        Genera una respuesta basada en los fragmentos recuperados.
        """
        context = "\n".join([chunk.page_content for chunk in context_chunks])

        prompt = (
            f"You are an AI assistant specialized in generating a valid prompt for stabilityai/stable-diffusion-2-1 to illustrate this topic: {query}, taking into account the context provided.\n"
"You must provide only the English prompt as a response.\n"
f"**Context:**\n{context}\n\n"
"Example response: Portrait of a female programmer working in an office using an AI assistant, modern office environment, bright daylight, computer and tablet screens showing AI related data and algorithms."
"You can only use a maximum of 77 tokens. Your interlocutor is the stable diffusion model, so skip phrases like 'Here is a valid prompt for stabilityai/stable-diffusion-2-1:'")     
        print(f"\n{BRIGHT_GREEN}{STAR} PROMPT {STAR}{RESET}")
        print(f"\n{TURQUOISE}{prompt}{RESET}\n")

        completion = self.llm_client.chat.completions.create(
            model=self.llm_model_name,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stop=None,
        )
        return completion.choices[0].message.content


