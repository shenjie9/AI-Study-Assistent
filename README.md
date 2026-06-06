# AI Study Assistant

A Retrieval-Augmented Generation (RAG) system that allows users to query PDF lecture notes using natural language.

## Features

* PDF text extraction using PyMuPDF
* Overlapping document chunking
* Semantic embeddings using SentenceTransformers
* Vector similarity search using FAISS
* Local LLM inference using Llama 3.2 via Ollama
* Retrieval-Augmented Generation (RAG) pipeline

## Demo Dataset

This repository includes `csc311_study_notes.pdf`, a set of machine learning study notes used to demonstrate the system.

The assistant is not limited to this document. Any PDF can be substituted and processed through the same pipeline.

## Architecture

PDF
→ Text Extraction
→ Chunking
→ Embeddings
→ FAISS Vector Search
→ Llama 3.2
→ Answer Generation

## Technologies

* Python
* PyMuPDF
* SentenceTransformers
* FAISS
* Ollama
* Llama 3.2
