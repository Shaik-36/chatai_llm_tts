"""
FastAPI server setup with WebSocket support for LLM-TTS pipeline.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys

from src.websocket_handler import handle_websocket
from src.config import settings

# ================================================================
#  Server Lifecycle Handling
# ================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    print("\n[INFO] Starting LLM-TTS Server...!")
    print("[INFO] ✅ Ready for connections\n")
    
    yield
    
    # Shutdown
    print("\[INFO] 🛑 Shutting down...")

# ================================================================
#  Define FastAPI Server and Middleware
# ================================================================

app = FastAPI(
    title="LLM-TTS WebSocket Service",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================================================
#  Routes
# ================================================================

@app.get("/")
async def root():
    return JSONResponse({
        "service": "LLM-TTS WebSocket",
        "status": "running",
        "ws": "/ws",
        "docs": "/docs"
    })


@app.get("/health")
async def health():
    return JSONResponse({"status": "healthy"})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await handle_websocket(websocket)

# ================================================================
#  Uvicorn Server main - Useful for Multi-Processing
# ================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
