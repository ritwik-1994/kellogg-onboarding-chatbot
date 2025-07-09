# Kellogg Student Chat Assistant

End‑to‑end repo for a Retrieval‑Augmented Generation (RAG) chat assistant that lets incoming Kellogg School of Management students ask onboarding questions and receive citation‑backed answers from PDF slide decks and WhatsApp group chat exports.

**Main stacks**

* **Backend** FastAPI + [Cline](https://github.com/run-llama/cline) + Postgres/pgvector + Llama.cpp
* **Frontend** Next.js (React) + Tailwind + shadcn/ui
* **Dev env** GitHub Codespaces (see `.devcontainer/`)

## Quick Start (in Codespaces)

1. **Launch Codespaces** (or `devcontainer open` locally) – the container will auto‑download the 7‑B GGUF model and embedding weights on first run.
2. **Start Postgres**  
   ```bash
   docker compose up -d db
   ```
3. **Run backend**  
   ```bash
   uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. **Ingest sample data**  
   ```bash
   python backend/app/ingest.py data/sample/
   ```
5. **Start frontend**  
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Open the forwarded port (default **3000**).

## Folder Layout

```
.devcontainer/          # Codespaces definition
backend/                # FastAPI + Cline service
frontend/               # Next.js UI
data/                   # place PDFs and WhatsApp exports here
docker-compose.yml      # Postgres + backend helper
README.md
```

## Production Hint
Use the provided Docker Compose file (`docker compose up --build`) to run Postgres and the backend together.  
Deploy the frontend separately (e.g. Vercel) and point `NEXT_PUBLIC_API_URL` to the backend URL.
