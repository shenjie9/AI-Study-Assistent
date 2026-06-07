# AI Study Assistant

A Retrieval-Augmented Generation (RAG) system that enables users to query PDF documents using natural language. The system combines semantic retrieval, vector search, and large language models to generate context-aware answers grounded in the uploaded document.

## Features

* PDF text extraction using PyMuPDF
* Intelligent document chunking for long-form content
* Semantic embeddings using SentenceTransformers
* Cosine similarity vector search with FAISS
* Retrieval-Augmented Generation (RAG) pipeline
* Local LLM support through Ollama and Llama 3.2
* Cloud LLM support through OpenAI models
* Provider-based architecture for interchangeable LLM backends
* Source-grounded responses generated from retrieved document context

## Demo Dataset

This repository includes `csc311_study_notes.pdf`, a set of machine learning study notes used to demonstrate the system.

The assistant is not limited to this document. Any PDF can be processed through the same pipeline, making the system applicable to lecture notes, textbooks, research papers, technical documentation, and other knowledge sources.

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

## Technologies

### Core AI & Machine Learning

* SentenceTransformers
* FAISS
* Llama 3.2
* OpenAI API

### Backend

* Python
* Requests
* FastAPI (planned)

### Document Processing

* PyMuPDF

### Architecture & Design

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases
* Provider Abstraction Pattern
* Dependency Injection

## Key Concepts Implemented

* Retrieval-Augmented Generation (RAG)
* Document Chunking Strategies
* Embedding Models
* Cosine Similarity Search
* Vector Indexing with FAISS
* Local LLM Deployment
* Cloud LLM Integration
* Context-Aware Prompt Engineering