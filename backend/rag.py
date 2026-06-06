import fitz
import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_text_from_pdf(pdf_path):
    """
    Extract all text from a PDF.
    """
    document = fitz.open(pdf_path)
    text = ""

    for page in document:
        text += page.get_text()

    document.close()
    return text


def chunk_text(text, chunk_size=800, overlap=150):
    """
    Split text into overlapping chunks.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks

"""FAISS search using L2 distance 
def create_vector_store(chunks):
    embeddings = embedding_model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index, chunks


def retrieve_relevant_chunks(question, index, chunks, top_k=3):
    question_embedding = embedding_model.encode([question])
    question_embedding = np.array(question_embedding).astype("float32")
    distances, indices = index.search(question_embedding, top_k)

    relevant_chunks = []

    for i in indices[0]:
        relevant_chunks.append(chunks[i])

    return relevant_chunks
"""

def create_vector_store(chunks):
    """
    Convert chunks into embeddings and store them in a FAISS index using cosine similarity.
    """
    embeddings = embedding_model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")

    # Normalize vectors so inner product becomes cosine similarity
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    # Inner product on normalized vectors = cosine similarity
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return index, chunks


def retrieve_relevant_chunks(question, index, chunks, top_k=4):
    """
    Retrieve the chunks most semantically similar to the user's question.
    """
    question_embedding = embedding_model.encode([question])
    question_embedding = np.array(question_embedding).astype("float32")

    # Normalize question vector for cosine similarity
    faiss.normalize_L2(question_embedding)

    similarities, indices = index.search(question_embedding, top_k)

    relevant_chunks = []

    for i in indices[0]:
        relevant_chunks.append(chunks[i])

    return relevant_chunks

def generate_answer(question, relevant_chunks):

    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are an AI study assistant.

Use ONLY the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    return response.json()["response"]