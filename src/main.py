"""
Main Application Entry Point

This is where the FastAPI application is created and configured.

Responsibilities:
1. Create FastAPI app instance
2. Configure CORS (allow browser clients)
3. Register routes (WebSocket, health check, info)
4. Wire routes to handlers
5. Provide startup validation

This file does NOT contain business logic - it just wires things together.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.websocket_handler import handle_websocket
from src.config import settings


# ========================================
# LIFESPAN EVENT HANDLER (Modern Way)
# ========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    This is the modern FastAPI way to handle application lifecycle.
    Replaces deprecated @app.on_event("startup") and @app.on_event("shutdown").
    
    Structure:
    - Code before yield = runs on startup
    - yield = application runs
    - Code after yield = runs on shutdown
    """
    
    # ==================== STARTUP ====================
    print("=" * 60)
    print("🚀 LLM-TTS WebSocket Service Starting...")
    print("=" * 60)
    
    # Validate critical configuration
    # If these are missing, fail immediately (don't wait for first request)
    try:
        # This will raise ValidationError if OPENAI_API_KEY missing
        _ = settings.openai_api_key
        print(f"✅ OpenAI API Key: Configured")
    except Exception as e:
        print(f"❌ Configuration Error: {e}")
        print("⚠️  Set OPENAI_API_KEY in .env file")
        raise  # Stop server startup
    
    # Log configuration (helps with debugging)
    print(f"📊 Configuration:")
    print(f"   - LLM Model: {settings.llm_model}")
    print(f"   - TTS Model: {settings.tts_model}")
    print(f"   - TTS Voice: {settings.tts_voice}")
    print(f"   - Max Tokens: {settings.llm_max_tokens}")
    print(f"   - Temperature: {settings.llm_temperature}")
    print(f"   - Request Timeout: {settings.request_timeout}s")
    
    print(f"\n🌐 Server Info:")
    print(f"   - Host: {settings.host}")
    print(f"   - Port: {settings.port}")
    print(f"   - WebSocket: ws://{settings.host}:{settings.port}/ws")
    # For Production you can replace with your domain name
    print(f"   - Health Check: http://localhost:{settings.port}/health")
    print(f"   - Documentation: http://localhost:{settings.port}/docs")
    
    print("=" * 60)
    print("✅ Startup Complete - Ready for Connections!")
    print("=" * 60)
    
    # ==================== APPLICATION RUNS ====================
    yield  # Server runs here, handling requests
    
    # ==================== SHUTDOWN ====================
    print("\n" + "=" * 60)
    print("🛑 LLM-TTS WebSocket Service Shutting Down...")
    print("=" * 60)
    
    # We don't have persistent resources to clean up
    # (httpx clients are context-managed per request)
    # But this section is here for future extensions
    
    print("✅ Shutdown Complete")
    print("=" * 60)


# ========================================
# APPLICATION CREATION
# ========================================

app = FastAPI(
    title="LLM-TTS WebSocket Service",
    description="Real-time ChatAI LLM-TTS via WebSocket",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI available at /docs
    redoc_url="/redoc",  # ReDoc available at /redoc
    lifespan=lifespan  # Register lifespan handler
)


# ========================================
# CORS CONFIGURATION
# ========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    # In production, replace with specific origins:
    # allow_origins=["https://yourdomain.com", "https://app.yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Why CORS?
# - Browsers block cross-origin WebSocket connections by default
# - This allows clients served from different domains to connect
# - Essential for local development (file:// protocol, different ports)
#
# Security note:
# - allow_origins=["*"] is permissive (OK for dev/demo)
# - Production should whitelist specific domains


# ========================================
# ROUTES
# ========================================

@app.get("/")
async def root():
    """
    Root endpoint - Service information.
    
    Useful for:
    - Quickly checking if service is running
    - Seeing configuration (which models being used)
    - Onboarding new developers
    
    Returns:
        JSON with service info and configuration
    """
    return JSONResponse({
        "service": "LLM-TTS WebSocket Service",
        "status": "running",
        "websocket_endpoint": "/ws",
        "health_check": "/health",
        "documentation": "/docs",
        "config": {
            "llm_model": settings.llm_model,
            "tts_model": settings.tts_model,
            "tts_voice": settings.tts_voice,
            "max_tokens": settings.llm_max_tokens,
        }
    })

# Why include config in response?
# - Transparency: clients know which models are being used
# - Debugging: easy to verify configuration without checking logs
# - Documentation: self-describing API


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Used by:
    - Load balancers (AWS ELB, k8s probes)
    - Monitoring systems (Datadog, New Relic)
    - CI/CD pipelines (check if deployment succeeded)
    
    Should be fast (<100ms) and lightweight.
    
    Returns:
        JSON with status=healthy
    """
    return JSONResponse({
        "status": "healthy",
        "service": "LLM-TTS WebSocket Service"
    })

# Why separate from root endpoint?
# - Standard practice: /health is specifically for health checks
# - Load balancers look for /health by convention
# - Can add more complex checks later (DB connection, API reachability)
#
# What makes a good health check?
# - Fast (no heavy computations)
# - Lightweight (no external API calls)
# - Clear signal (200 OK = healthy, anything else = unhealthy)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Main WebSocket endpoint for LLM-TTS pipeline.
    
    Flow:
    1. Client connects to ws://host:port/ws
    2. Connection handed to websocket_handler
    3. Handler manages message loop until disconnect
    
    Protocol:
    - Client sends: {"text": "user input"}
    - Server sends: {"type": "audio", "audio_data": "base64...", "llm_text": "..."}
    - Or error: {"type": "error", "error_message": "..."}
    
    See src/models.py for full message format specification.
    """
    # Delegate all logic to the handler
    # This endpoint is just the "front door" - actual logic in websocket_handler
    await handle_websocket(websocket)

# Why delegate to handle_websocket?
# - Separation of concerns:
#   - main.py: routing and configuration
#   - websocket_handler.py: business logic
# - Easier testing: can test handler without FastAPI
# - Cleaner: this file stays focused on app setup


# ========================================
# DEVELOPMENT SERVER RUNNER
# ========================================

if __name__ == "__main__":
    """
    Development server runner.
    
    Allows running directly: python -m src.main
    
    For production, use: uvicorn src.main:app --host 0.0.0.0 --port 8000
    """
    import uvicorn
    
    # Run with hot-reload enabled (watches for file changes)
    uvicorn.run(
        "src.main:app",  # Import string (allows hot-reload)
        host=settings.host,
        port=settings.port,
        reload=True,  # Hot-reload on code changes (dev only)
        log_level="info"
    )

# Why support both direct run and uvicorn command?
# - Direct run (python -m src.main): convenient for development
# - Uvicorn command: standard for production, more control
# - Flexibility: works in different environments
