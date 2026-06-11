# AI Study Assistant

A FastAPI-powered Retrieval-Augmented Generation (RAG) application that enables users to upload PDF documents and query them using local or cloud-based large language models.

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

## Architecture

```text
User
 ↓
FastAPI REST API
 ↓
PDF Upload Endpoint
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
Provider Abstraction Layer
    ├─ Ollama (Llama 3.2)
    └─ OpenAI (GPT Models)
 ↓
Answer Generation
```

---

## Software Architecture & Multi-Provider LLM Design

The system is designed around an abstract `LLMProvider` interface, allowing different language model backends to be swapped without modifying the Retrieval-Augmented Generation (RAG) pipeline.

Currently implemented providers:

* `OllamaProvider` — local inference using Llama 3.2 through Ollama
* `OpenAIProvider` — cloud-based inference through the OpenAI API

This architecture separates document retrieval from language model inference, ensuring that chunking, embedding generation, vector search, and retrieval logic remain independent of the underlying model implementation.

The design demonstrates several software engineering principles:

* Dependency Inversion Principle
* Interface-Based Architecture
* Separation of Concerns
* Extensible Backend Design

At present, the project is configured for local inference through Ollama. OpenAI integration has been implemented but is not enabled by default because an API key has not been provisioned for this repository. Once credentials are supplied, the OpenAI provider can be selected without requiring any changes to the RAG pipeline.

---

## Technologies

### Core AI & Machine Learning

* SentenceTransformers
* FAISS
* Llama 3.2
* OpenAI API

### Backend & APIs

* Python
* FastAPI
* REST APIs
* OpenAPI / Swagger
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

## Demo Dataset

This repository includes `csc311_study_notes.pdf`, a set of machine learning study notes used to demonstrate the system.

The assistant is not limited to this document. Any PDF can be processed through the same pipeline, making the system applicable to lecture notes, textbooks, research papers, technical documentation, and other knowledge sources.

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

## Quick Start

```bash
chmod +x run_backend.sh
./run_backend.sh
```

The startup script:

1. Starts the Ollama server
2. Waits for Ollama to become available
3. Launches the FastAPI backend

Once running, open the forwarded port in your browser to access the interactive API documentation.

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

## API Endpoints

| Endpoint | Description |
|-----------|-------------|
| GET /health | Service health check |
| POST /upload | Upload and index a PDF |
| POST /ask | Query the indexed document |

---

## Command-Line Testing

The original command-line prototype can still be executed:

```bash
python backend/test_rag.py
```

---

## Project Structure

```text
AI-Study-Assistant/
│
├── backend/
│   ├── main.py
│   ├── rag.py
│   ├── test_rag.py
│   ├── requirements.txt
│   ├── csc311_study_notes.pdf
│   └── llm/
│       ├── provider.py
│       ├── factory.py
│       ├── ollama_provider.py
│       └── openai_provider.py
│
├── frontend/
├── run_backend.sh
├── .gitignore
└── README.md
```

---


