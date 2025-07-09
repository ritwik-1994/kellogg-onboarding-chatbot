#!/usr/bin/env bash
set -e

echo "⬇️  Downloading Mistral-7B GGUF model (Q4_K_M)…"
MODEL_URL="https://huggingface.co/mistralai/Mistral-small-2506-GGUF/resolve/main/mistral-small-2506.Q4_K_M.gguf"
mkdir -p $MODEL_DIR
curl -L $MODEL_URL -o $MODEL_DIR/mistral-small.Q4_K_M.gguf

echo "⬇️  Downloading embedding model…"
python - <<'PY'
from sentence_transformers import SentenceTransformer
SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
PY

echo "✅ Bootstrap complete"
