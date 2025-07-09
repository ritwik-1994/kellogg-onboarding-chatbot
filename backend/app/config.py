import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pg:pg@db:5432/vecdb")
MODEL_PATH = os.getenv("MODEL_PATH", "/workspace/models/mistral-small.Q4_K_M.gguf")
