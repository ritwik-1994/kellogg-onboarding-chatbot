FROM mcr.microsoft.com/devcontainers/python:3.12

RUN apt-get update && apt-get install -y build-essential cmake git curl postgresql-client

# llama.cpp build (CPU/OpenBLAS)
RUN pip install --no-cache-dir llama-cpp-python==0.2.61 \
    fastapi uvicorn cline[pg] sentence-transformers==2.7.0 \
    pdfminer.six==20221105 python-magic[pathtype] pandas typer slowapi psycopg2-binary

RUN pip install --no-cache-dir fastapi uvicorn cline[pg] sentence-transformers==2.7.0 \
  pdfminer.six==20221105 python-magic[pathtype] pandas typer slowapi psycopg2-binary

ENV MODEL_DIR=/workspace/models
RUN mkdir -p $MODEL_DIR && chown -R vscode:vscode $MODEL_DIR

USER vscode
