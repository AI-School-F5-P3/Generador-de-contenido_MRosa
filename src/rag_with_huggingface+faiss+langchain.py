from langchain_community.document_loaders import HuggingFaceDatasetLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import RetrievalQA
import pandas as pd
import os
from huggingface_hub import HfFolder
from langchain.schema import Document


import torch
print(f"\n\n===============================================================================\n\nCUDA -------- > {torch.cuda.is_available()}\n\n===============================================================================\n\n")
print(torch.cuda.is_available())


# that's already defined in your Python environment.
HfFolder.save_token("HF_TOKEN") # Guarda el token usando la variable  HF_TOKEN

df = pd.read_json("hf://datasets/databricks/databricks-dolly-15k/databricks-dolly-15k.jsonl", lines=True)
# Display the first 2 entries
print(f"\n\n===============================================================================\n\n{df[:2]}\n\n===============================================================================\n\n")

# Transformar cada fila del DataFrame en un objeto Document
data = [
    Document(
        metadata={
            "instruction": row["instruction"],
            "response": row["response"],
            "category": row["category"]
        },
        page_content=row["context"]
    )
    for _, row in df.iterrows()
]
 

print(f"\n\n===============================================================================\n\n{data[:2]}\n\n===============================================================================\n\n")


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)

# 'data' holds the text you want to split, split the text into documents using the text splitter.
docs = text_splitter.split_documents(data)

# Define the path to the pre-trained model you want to use
# modelPath = "sentence-transformers/all-MiniLM-L6-v2"
modelPath = "sentence-transformers/all-mpnet-base-v2"

# Create a dictionary with model configuration options, specifying to use the CUDA for computations
model_kwargs = {'device': 'cpu'}

# Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
encode_kwargs = {'normalize_embeddings': False}
print(f"\n\n===============================================================================\n\n{encode_kwargs}\n\n===============================================================================\n\n")

# Initialize an instance of HuggingFaceEmbeddings with the specified parameters
embeddings = HuggingFaceEmbeddings(
    model_name=modelPath,         # Provide the pre-trained model's path
    model_kwargs=model_kwargs,    # Pass the model configuration options
    encode_kwargs=encode_kwargs   # Pass the encoding options
)
print(f"\n\n===============================================================================\n\n{embeddings}\n\n===============================================================================\n\n")

# Example of embedding a query
text = "This is a test document."
query_result = embeddings.embed_query(text)


print(f"\n\n==================================== query_result[:3] ===========================================\n\n{query_result[:3]}\n\n===============================================================================\n\n")


db = FAISS.from_documents(docs, embeddings)

print(f"db.embeddings -------------> {db.embeddings}")


question = "What is cheesemaking?"
searchDocs = db.similarity_search(question)
print(searchDocs[0].page_content)

# Specify the model name you want to use
model_name = "Intel/dynamic_tinybert"

# Load the tokenizer associated with the specified model
tokenizer = AutoTokenizer.from_pretrained(model_name, padding=True, truncation=True, max_length=512)

# Define a question-answering pipeline using the model and tokenizer
question_answerer = pipeline(
    "question-answering",
    model=model_name,
    tokenizer=tokenizer,
    return_tensors="pt"
)

# Create an instance of the HuggingFacePipeline, which wraps the question-answering pipeline
# with additional model-specific arguments (temperature and max_length)
llm = HuggingFacePipeline(
    pipeline=question_answerer,
    model_kwargs={"temperature": 0.7, "max_length": 512},
)

# Recuperar datos o documentos de la base de datos.
retriever = db.as_retriever()

docs = retriever.get_relevant_documents("What is Machine learning?")
print(f'recuperar datos o documentos de la base de datos {docs[0].page_content}')

# Crea un objeto retriever desde 'db' con una configuración de búsqueda donde recupera hasta 4 divisiones/documentos relevantes.
retriever = db.as_retriever(search_kwargs={"k": 4})
print(f'retriever {retriever}')

# Crea una instancia de preguntas y respuestas (qa) usando la clase RetrievalQA.
# Está configurado con un modelo de lenguaje (llm), un tipo de cadena "refine", el retriever que creamos y una opción para no devolver documentos de origen.
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="refine", retriever=retriever, return_source_documents=False)
print(f'qa {qa}')

# Recuperar los documentos relevantes
question = "Who is Thomas Jefferson?"
docs = retriever.get_relevant_documents(question)

# Extraer el contenido del primer documento como contexto
if docs:
    context_str = docs[0].page_content
    print("Context:", context_str)
else:
    print("No relevant documents found.")
    context_str = ""

if context_str:  # Nos aseguramos de qu hay un contexto disponible
    result = question_answerer(question=question, context=context_str)
    print("Answer:", result["answer"])
else:
    print("No context available for answering the question.")

def answer_question(question, retriever, question_answerer):
    """
    Responde una pregunta utilizando un retriever para obtener el contexto y un question_answerer para generar la respuesta.

    Args:
        question (str): La pregunta que se desea responder.
        retriever: El objeto retriever para obtener documentos relevantes.
        question_answerer: El pipeline de Hugging Face para generar respuestas.

    Returns:
        str: La respuesta generada o un mensaje indicando que no se encontró contexto.
    """
    # Recuperar documentos relevantes
    docs = retriever.get_relevant_documents(question)

    # Extraer el contenido del primer documento como contexto
    if docs:
        context_str = docs[0].page_content
        # print("Context:", context_str)
    else:
        print("No relevant documents found.")
        context_str = ""

    # Generar respuesta si hay contexto
    if context_str:
        result = question_answerer(question=question, context=context_str)
        return result["answer"]
    else:
        return "No context available for answering the question."

question = "Where was Tomoaki Komorida born?"
answer = answer_question(question, retriever, question_answerer)
print("Answer:", answer)

question = "What do you know about Thomas Jefferson?"
answer = answer_question(question, retriever, question_answerer)
print("Answer:", answer)