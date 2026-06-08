# AI Study Assistant

A Retrieval-Augmented Generation (RAG) system that enables users to query PDF documents using natural language. The system combines semantic retrieval, vector search, and large language models to generate context-aware answers grounded in uploaded documents.

---

## Features

* PDF text extraction using PyMuPDF
* Intelligent document chunking for long-form content
* Semantic embeddings using SentenceTransformers
* Cosine similarity vector search with FAISS
* Retrieval-Augmented Generation (RAG) pipeline
* FastAPI backend with interactive API documentation
* Local LLM support through Ollama and Llama 3.2
* Cloud LLM support through OpenAI models
* Provider-based architecture for interchangeable LLM backends
* Source-grounded responses generated from retrieved document context

---

## Demo Dataset

This repository includes `csc311_study_notes.pdf`, a set of machine learning study notes used to demonstrate the system.

The assistant is not limited to this document. Any PDF can be processed through the same pipeline, making the system applicable to lecture notes, textbooks, research papers, technical documentation, and other knowledge sources.

---

## Architecture

```text
PDF Document
      ↓
Text Extraction (PyMuPDF)
      ↓
Document Chunking
      ↓
Embedding Generation
      ↓
FAISS Vector Index
      ↓
Cosine Similarity Retrieval
      ↓
Context Construction
      ↓
LLM Provider
   ├─ Ollama (Llama 3.2)
   └─ OpenAI (GPT Models)
      ↓
Answer Generation
```

---

## Technologies

### Core AI & Machine Learning

* SentenceTransformers
* FAISS
* Llama 3.2
* OpenAI API

### Backend

* Python
* FastAPI
* Requests

### Document Processing

* PyMuPDF

### Architecture & Design

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases
* Provider Abstraction Pattern
* Dependency Injection

---

## Key Concepts Implemented

* Retrieval-Augmented Generation (RAG)
* Document Chunking Strategies
* Embedding Models
* Cosine Similarity Search
* Vector Indexing with FAISS
* Local LLM Deployment
* Cloud LLM Integration
* Context-Aware Prompt Engineering

---

## Multi-Provider LLM Architecture

The system is designed around an abstract `LLMProvider` interface, allowing different language model backends to be swapped without modifying the Retrieval-Augmented Generation (RAG) pipeline.

Currently implemented providers:

* `OllamaProvider` — local inference using Llama 3.2 through Ollama
* `OpenAIProvider` — cloud-based inference through the OpenAI API

The provider abstraction follows the Dependency Inversion Principle, ensuring that retrieval, chunking, embedding generation, and vector search remain independent of the underlying language model.

At present, the project is configured for local inference through Ollama. OpenAI integration has been implemented but is not enabled by default because an API key has not been provisioned for this repository. Once credentials are supplied, the OpenAI provider can be selected without requiring any changes to the RAG pipeline.

---

# Running the Project

## Requirements

* Python 3.12+
* Ollama
* Git

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

---

## Local LLM Setup (Ollama)

Start the Ollama server:

```bash
ollama serve
```

Pull the default model:

```bash
ollama pull llama3.2:1b
```

> Note: The project also supports OpenAI through an interchangeable provider interface, but an API key is required and is not included in this repository.

---

## Running the FastAPI Backend

Open a second terminal and run:

```bash
cd backend
uvicorn main:app --reload
```

You should see:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

## Interactive API Documentation

FastAPI automatically generates Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

The API exposes three endpoints:

### GET /health

Health-check endpoint.

Returns:

```json
{
  "status": "ok"
}
```

### POST /upload

Uploads and indexes a PDF document.

Input:

* PDF file

Returns:

```json
{
  "message": "PDF uploaded and indexed successfully.",
  "filename": "example.pdf",
  "chunks_created": 44
}
```

### POST /ask

Queries the uploaded document using Retrieval-Augmented Generation.

Input:

* `question`
* `provider_name` (`ollama` or `openai`)

Returns:

```json
{
  "question": "...",
  "provider": "ollama",
  "answer": "...",
  "retrieved_chunks": [...]
}
```

---

## Command-Line Testing

The original command-line prototype can still be executed:

```bash
python backend/test_rag.py
```

This workflow:

1. Extracts text from the PDF
2. Creates document chunks
3. Generates embeddings
4. Builds a FAISS vector index
5. Retrieves relevant chunks
6. Generates an answer using the selected LLM provider

---

## Project Structure

```text
AI-Study-Assistant/
│
├── backend/
│   ├── main.py
│   ├── rag.py
│   ├── test_rag.py
│   ├── csc311_study_notes.pdf
│   └── llm/
│       ├── provider.py
│       ├── factory.py
│       ├── ollama_provider.py
│       └── openai_provider.py
│
├── frontend/
│
├── README.md
└── requirements.txt
```

