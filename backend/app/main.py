from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from .rag import get_rag_chain

app = FastAPI(title="Kellogg Student Chat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    history: List[str] = []

@app.post("/chat")
async def chat(req: ChatRequest):
    rag = get_rag_chain()
    answer = rag.invoke(req.question)
    return answer

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    rag = get_rag_chain(stream=True)
    try:
        while True:
            user_msg = await ws.receive_text()
            async for chunk in rag.stream(user_msg):
                await ws.send_text(chunk)
    except WebSocketDisconnect:
        pass
