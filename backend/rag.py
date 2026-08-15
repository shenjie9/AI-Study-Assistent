import faiss
import pymupdf
import numpy as np
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF."""
    document = pymupdf.open(pdf_path)
    text = ""

    for page in document:
        text += page.get_text()

    document.close()
    return text


def chunk_text(text, chunk_size=500, overlap=100):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks


def create_vector_store(chunks):
    """Embed chunks and store them in FAISS for cosine-similarity search."""
    embeddings = embedding_model.encode(chunks)
    embeddings = np.asarray(embeddings, dtype="float32")

    # Inner product on L2-normalized vectors is cosine similarity.
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return index, chunks


def retrieve_relevant_chunks(question, index, chunks, top_k=3):
    """Return the chunks most semantically similar to a question."""
    question_embedding = embedding_model.encode([question])
    question_embedding = np.asarray(question_embedding, dtype="float32")
    faiss.normalize_L2(question_embedding)

    _, indices = index.search(question_embedding, min(top_k, len(chunks)))
    return [chunks[i] for i in indices[0] if 0 <= i < len(chunks)]


def build_prompt(question, relevant_chunks):
    """Build a context-grounded prompt for the selected LLM provider."""
    context = "\n\n".join(relevant_chunks)

    return f"""
You are an AI study assistant.

Answer the question using the provided context.

If the answer can be reasonably inferred from the context, provide the answer.
Only say "I could not find enough information in the uploaded notes to answer this."
if the answer truly does not appear in the context.

Context:
{context}

Question:
{question}

Answer:
""".strip()


def generate_answer(question, relevant_chunks, provider):
    """Generate an answer using the selected LLM provider."""
    relevant_chunks = [chunk[:1000] for chunk in relevant_chunks]
    prompt = build_prompt(question, relevant_chunks)
    return provider.generate(prompt)
