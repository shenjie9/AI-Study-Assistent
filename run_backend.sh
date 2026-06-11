#!/bin/bash

echo "Starting Ollama server..."
ollama serve > ollama.log 2>&1 &

echo "Waiting for Ollama to start..."
until curl -s http://localhost:11434 > /dev/null; do
    sleep 1
done

echo "Starting FastAPI backend..."
cd backend
uvicorn main:app --reload

# to make executable: chmod +x run_backend.sh
# to run, use: ./run_backend.sh