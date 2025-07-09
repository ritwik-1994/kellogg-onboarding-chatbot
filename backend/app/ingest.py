import typer, os, glob, json
from pathlib import Path
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
import psycopg2
from psycopg2.extras import Json
from .config import DATABASE_URL
from .parsers import parse_pdf, parse_whatsapp

app = typer.Typer(help="ETL utility to ingest documents into pgvector")

EMBED_MODEL = "all-MiniLM-L6-v2"
chunk_size = 384

def connect():
    return psycopg2.connect(DATABASE_URL)

def upsert_chunks(records):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    cur.execute(
        """CREATE TABLE IF NOT EXISTS chunks(
            id SERIAL PRIMARY KEY,
            embedding vector(384),
            text TEXT,
            metadata JSONB
        )"""
    )
    args_str = ",".join(
        cur.mogrify("(%s,%s,%s)", (emb.tolist(), txt, Json(meta))).decode()
        for (emb, txt, meta) in records
    )
    cur.execute(
        "INSERT INTO chunks (embedding, text, metadata) VALUES " + args_str
    )
    conn.commit()
    cur.close()
    conn.close()

@app.command()
def run(path: str = typer.Argument(..., help="Folder or file to ingest")):
    p = Path(path)
    files: List[Path] = []
    if p.is_dir():
        files = list(p.glob("**/*"))
    else:
        files = [p]

    model = SentenceTransformer(EMBED_MODEL)

    batch_records = []

    for file in files:
        if file.suffix.lower() == ".pdf":
            docs = parse_pdf(file)
        elif file.suffix.lower() in {".txt", ".csv"}:
            docs = parse_whatsapp(file)
        else:
            continue

        for d in docs:
            emb = model.encode(d["text"])
            batch_records.append((emb, d["text"], d["metadata"]))

    if batch_records:
        upsert_chunks(batch_records)
        typer.echo(f"Ingested {len(batch_records)} chunks ✅")
    else:
        typer.echo("No supported files found.")

if __name__ == "__main__":
    app()
