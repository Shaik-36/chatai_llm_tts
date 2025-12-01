"""
Main Application Entry Point

FastAPI server setup with WebSocket support for LLM-TTS pipeline.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys

from src.websocket_handler import handle_websocket
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle."""
    
    # Startup
    print("\n🚀 Starting LLM-TTS Service")
    
    try:
        _ = settings.openai_api_key
        print("✅ Configuration loaded")
        print(f"   LLM:     {settings.llm_model}")
        print(f"   TTS:     {settings.tts_model}")
        print(f"   Server:  http://localhost:{settings.port}")
        print(f"   OpenAPI: http://localhost:{settings.port}/docs")
    except Exception as e:
        print(f"❌ Config error: {e}")
        sys.exit(1)
    
    print("✅ Ready for connections\n")
    
    yield
    
    # Shutdown
    print("\n🛑 Shutting down...")


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


@app.get("/")
async def root():
    """Service info endpoint."""
    return JSONResponse({
        "service": "LLM-TTS WebSocket",
        "status": "running",
        "ws": "/ws",
        "docs": "/docs"
    })


@app.get("/health")
async def health():
    """Health check."""
    return JSONResponse({"status": "healthy"})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint - routes to handler."""
    await handle_websocket(websocket)


if __name__ == "__main__":
    import uvicorn
    
    print("💡 Press Ctrl+C to shutdown\n")
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
