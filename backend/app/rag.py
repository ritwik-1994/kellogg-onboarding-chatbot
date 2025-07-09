from functools import lru_cache
from cline.embeddings import LocalEmbeddingEncoder
from cline.llms import LlamaCppChat
from cline.vectorstores import PGVector
from cline.chains import RagChain
from .config import DATABASE_URL, MODEL_PATH

EMBED_MODEL = "all-MiniLM-L6-v2"

def _build_rag(stream: bool = False) -> RagChain:
    encoder = LocalEmbeddingEncoder(EMBED_MODEL)
    vs = PGVector(DATABASE_URL)
    llm = LlamaCppChat(
        model_path=MODEL_PATH,
        n_gpu_layers=0,
        context_window=8192,
        temperature=0.7,
        stream=stream,
    )
    return RagChain(
        retriever=vs.as_retriever(k=6, search_type="mmr"),
        llm=llm,
        citation_format="[{source}:{loc}]",
    )

@lru_cache()
def get_rag_chain(stream: bool = False) -> RagChain:
    return _build_rag(stream=stream)
