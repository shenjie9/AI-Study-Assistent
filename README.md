# AI Study Assistant

A full-stack Retrieval-Augmented Generation (RAG) prototype for asking natural-language questions about uploaded PDF documents. The project combines a React/Vite frontend with a FastAPI backend, semantic retrieval using SentenceTransformers + FAISS, and interchangeable LLM providers.

The default demo runs fully locally with Ollama and Llama 3.2. OpenAI integration is implemented behind the same provider interface and can be enabled by supplying API credentials.

## Features

- React + Vite frontend with responsive dark-mode UI
- PDF upload and indexing workflow
- PDF text extraction with PyMuPDF
- Overlapping document chunking
- SentenceTransformers embeddings (`all-MiniLM-L6-v2`)
- FAISS cosine-similarity retrieval
- Retrieval-Augmented Generation (RAG)
- FastAPI REST endpoints with Swagger/OpenAPI documentation
- Local inference with Ollama + Llama 3.2 1B
- Optional OpenAI provider through a shared provider abstraction
- Loading, success, error, and document-ready UI states

## Architecture

```text
Browser
  |
  v
React + Vite (localhost:5173)
  |
  | POST /upload, POST /ask
  v
FastAPI (127.0.0.1:8000)
  |
  +--> PyMuPDF text extraction
  +--> Document chunking
  +--> SentenceTransformers embeddings
  +--> FAISS cosine-similarity retrieval
  |
  v
LLM Provider Interface
  |-- OllamaProvider -> Llama 3.2:1b (default local demo)
  `-- OpenAIProvider -> OpenAI API (optional credentials)
```

The retrieval pipeline is independent of the inference provider, so the LLM backend can be changed without rewriting PDF processing, embedding, indexing, or retrieval logic.

## Tech Stack

**Frontend:** React, Vite, JavaScript, CSS, ESLint  
**Backend:** Python, FastAPI, Uvicorn, REST APIs  
**RAG / ML:** SentenceTransformers, FAISS, NumPy, PyMuPDF  
**LLMs:** Ollama + Llama 3.2:1b; optional OpenAI API

## Project Structure

```text
AI-Study-Assistant/
├── backend/
│   ├── llm/
│   │   ├── factory.py
│   │   ├── ollama_provider.py
│   │   ├── openai_provider.py
│   │   └── provider.py
│   ├── csc311_study_notes.pdf
│   ├── main.py
│   ├── rag.py
│   ├── requirements.txt
│   └── test_rag.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── QuestionForm.jsx
│   │   │   └── UploadPanel.jsx
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── config.js
│   │   ├── index.css
│   │   └── main.jsx
│   ├── .env.example
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .gitignore
├── README.md
└── run_backend.sh
```

## Prerequisites

Install:

- Python 3.12+
- Node.js + npm
- Ollama
- Git

The default local model is:

```bash
ollama pull llama3.2:1b
```

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd AI-Study-Assistant
```

### 2. Create the Python environment

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r backend/requirements.txt
```

### 3. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 4. Optional OpenAI configuration

Ollama works without cloud credentials. To enable the OpenAI provider, create a root `.env` file:

```text
OPENAI_API_KEY=your_api_key_here
```

Never commit the `.env` file or an API key to Git.

## Running the Application

Run the frontend and backend in two terminals.

### Terminal 1 — Backend

From the project root:

```bash
./run_backend.sh
```

The script uses the project's `.venv`, starts Ollama if needed, and launches FastAPI at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

### Terminal 2 — Frontend

```bash
cd frontend
npm run dev
```

Open:

```text
http://localhost:5173
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Backend health check |
| `POST` | `/upload` | Upload, parse, embed, and index a PDF |
| `POST` | `/ask` | Retrieve relevant chunks and generate an answer |

## Frontend Configuration

The frontend defaults to:

```text
http://127.0.0.1:8000
```

To use another backend URL, copy `frontend/.env.example` to `frontend/.env` and change:

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Demo Document

`backend/csc311_study_notes.pdf` is included as a reproducible example document. The application can process other text-based PDFs through the upload interface.

## Current Scope

This repository is intentionally a portfolio prototype rather than a production SaaS application. In its current form:

- one uploaded document is kept in memory at a time;
- the FAISS index is not persisted after the backend stops;
- the local 1B model prioritizes lightweight runtime over answer quality;
- OpenAI support requires a locally configured API key;
- authentication, user accounts, chat persistence, and multi-document workspaces are outside the current scope.

These constraints keep the project focused on demonstrating full-stack development, RAG architecture, semantic retrieval, API integration, and provider abstraction.

## Development Checks

Frontend lint:

```bash
cd frontend
npm run lint
```

Frontend production build:

```bash
npm run build
```

Command-line RAG prototype:

```bash
python backend/test_rag.py
```

## Security Notes

- API credentials belong in environment variables, never frontend source code.
- `.env`, virtual environments, `node_modules`, generated uploads, logs, and build output are excluded by `.gitignore`.
- CORS is limited to the local Vite development origins used by this prototype.
