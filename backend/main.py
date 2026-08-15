import os
import shutil

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from llm.factory import get_provider
from rag import (
    chunk_text,
    create_vector_store,
    extract_text_from_pdf,
    generate_answer,
    retrieve_relevant_chunks,
)

app = FastAPI(title="AI Study Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
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

    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        with open(UPLOAD_PATH, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text_from_pdf(UPLOAD_PATH)
        chunks = chunk_text(text)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No readable text was found in the uploaded PDF.",
            )

        vector_index, document_chunks = create_vector_store(chunks)
    finally:
        if os.path.exists(UPLOAD_PATH):
            os.remove(UPLOAD_PATH)

    return {
        "message": "PDF uploaded and indexed successfully.",
        "filename": filename,
        "chunks_created": len(chunks),
    }


@app.post("/ask")
async def ask_question(
    question: str = Form(...),
    provider_name: str = Form("ollama"),
):
    global vector_index, document_chunks

    if vector_index is None or document_chunks is None:
        raise HTTPException(status_code=400, detail="No PDF has been uploaded yet.")

    question = question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        provider = get_provider(provider_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    relevant_chunks = retrieve_relevant_chunks(
        question,
        vector_index,
        document_chunks,
    )

    answer = generate_answer(
        question,
        relevant_chunks,
        provider,
    )

    return {
        "question": question,
        "provider": provider_name,
        "answer": answer,
        "retrieved_chunks": relevant_chunks,
    }


@app.get("/")
def root():
    return RedirectResponse("/docs")
