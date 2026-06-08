import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from rag import (
    extract_text_from_pdf,
    chunk_text,
    create_vector_store,
    retrieve_relevant_chunks,
    generate_answer,
)

from llm.factory import get_provider


app = FastAPI(title="AI Study Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_PATH = "uploaded_document.pdf"

vector_index = None
document_chunks = None


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global vector_index, document_chunks

    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported."}

    with open(UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(UPLOAD_PATH)
    chunks = chunk_text(text)

    vector_index, document_chunks = create_vector_store(chunks)

    os.remove(UPLOAD_PATH)

    return {
        "message": "PDF uploaded and indexed successfully.",
        "filename": file.filename,
        "chunks_created": len(chunks),
    }


@app.post("/ask")
async def ask_question(
    question: str = Form(...),
    provider_name: str = Form("ollama")
):
    global vector_index, document_chunks

    if vector_index is None or document_chunks is None:
        return {"error": "No PDF has been uploaded yet."}

    relevant_chunks = retrieve_relevant_chunks(
        question,
        vector_index,
        document_chunks
    )

    provider = get_provider(provider_name)

    answer = generate_answer(
        question,
        relevant_chunks,
        provider
    )

    return {
        "question": question,
        "provider": provider_name,
        "answer": answer,
        "retrieved_chunks": relevant_chunks,
    }