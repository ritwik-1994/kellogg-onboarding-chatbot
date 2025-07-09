# .devcontainer/Dockerfile  – FINAL WORKING VERSION
FROM mcr.microsoft.com/devcontainers/python:3.12

# --------------------------------------------------------------------
# 1. OS-level dependencies
#    • build-essential & cmake  → compile llama-cpp-python wheel
#    • libopenblas-dev          → BLAS acceleration (optional but nice)
#    • git/curl/psql-client     → convenience utils
# --------------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential cmake git curl ca-certificates \
        libopenblas-dev postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------
# 2. Python packages
#    * llama-cpp-python wheel auto-compiles llama.cpp with CMake
#      (no manual clone/make needed)
# --------------------------------------------------------------------
RUN pip install --no-cache-dir \
        llama-cpp-python==0.2.61 \
        fastapi uvicorn cline[pg] \
        sentence-transformers==2.7.0 \
        pdfminer.six==20221105 python-magic[pathtype] \
        pandas typer slowapi psycopg2-binary

# --------------------------------------------------------------------
# 3. Non-root workspace setup
# --------------------------------------------------------------------
ENV MODEL_DIR=/workspace/models
RUN mkdir -p $MODEL_DIR && chown -R vscode:vscode $MODEL_DIR

USER vscode
