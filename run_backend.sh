#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$ROOT_DIR/.venv/bin/python"

if ! command -v ollama >/dev/null 2>&1; then
  echo "Error: Ollama is not installed or is not available on PATH."
  echo "Install Ollama, then pull the default model with: ollama pull llama3.2:1b"
  exit 1
fi

if [ ! -x "$PYTHON" ]; then
  echo "Error: Python virtual environment not found at $ROOT_DIR/.venv"
  echo "Create it with: python3 -m venv .venv"
  echo "Then install dependencies with: .venv/bin/python -m pip install -r backend/requirements.txt"
  exit 1
fi

if ! curl -fsS http://localhost:11434/api/tags >/dev/null 2>&1; then
  echo "Starting Ollama server..."
  ollama serve > "$ROOT_DIR/ollama.log" 2>&1 &

  echo "Waiting for Ollama to start..."
  until curl -fsS http://localhost:11434/api/tags >/dev/null 2>&1; do
    sleep 1
  done
else
  echo "Ollama server is already running."
fi

if ! ollama list | grep -q '^llama3.2:1b'; then
  echo "Warning: llama3.2:1b is not installed."
  echo "Run: ollama pull llama3.2:1b"
fi

echo "Starting FastAPI backend..."
cd "$ROOT_DIR/backend"
exec "$PYTHON" -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
