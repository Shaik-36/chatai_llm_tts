# LLM-TTS WebSocket Chat

Real-time text-to-speech chat using OpenAI APIs.

## Setup

### Prerequisites
- Python 3.9+
- OpenAI API key

### Installation

#### Clone the repo
```bash
git clone https://github.com/Shaik-36/llm_tts_websocket_chat.git
cd llm_tts_websocket_chat
```

#### Create a Virtual Environment

```bash
python -m venv venv   # Windows
python3 -m venv venv  # Mac
```
#### Activate the Virtual Environment

```bash
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Mac
```
#### Install the dependencies
```bash
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
# Edit .env and replace with your OPENAI_API_KEY=sk-your-key
```
**OpenAI API Platform:**
Open `https://platform.openai.com/api-keys`

## Running the app

**Terminal 1 - Server:**
```bash
python -m src.main    # Windows
python3 -m src.main   # Mac
```
or

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```



**Terminal 2 - Client:**

```bash
cd client
python -m http.server 5000   # Windows
python3 -m http.server 5000  # Mac
```

**Browser:**
Open `http://localhost:5000`


## Architecture

- **Server:** FastAPI WebSocket on port 8000
- **Client:** HTML/JS on port 5000
- **LLM:** OpenAI Chat Completions API
- **TTS:** OpenAI Text-to-Speech API

## How It Works

1. User types a message in the browser and clicks Send
2. Message is transmitted over `WebSocket` to the FastAPI server
3. Server validates the input using Pydantic models
4. Server forwards text to OpenAI Chat API to generate a response
5. Generated response is sent to OpenAI Text-to-Speech API
6. TTS API returns MP3 audio bytes
7. Server `encodes` audio to base64 and sends back to client
8. Client `decodes` audio and plays it automatically while displaying the text

**Flow Diagram:**
```
Browser → WebSocket → Server → OpenAI Chat API → Response
                        ↓
                    OpenAI TTS API → Audio
                        ↓
                    WebSocket → Browser → Play Audio
```

## File Structure

```
src/
  ├── main.py              # FastAPI app, routes, lifecycle
  ├── config.py            # Configuration from .env
  ├── models.py            # Pydantic validation models
  ├── websocket_handler.py # WebSocket connection & orchestration
  ├── llm_service.py       # OpenAI Chat API integration
  └── tts_service.py       # OpenAI Speech API integration

client/
  ├── index.html           # Web UI (minimal)
  └── script.js            # WebSocket client logic

tests/
  ├── test_models.py       # Model validation tests
  ├── test_websocket.py    # WebSocket endpoint tests
  ├── test_tts_service.py  # TTS service integration tests
  └── test_llm_service.py  # LLM service integration tests

requirements.txt           # Python dependencies
.env.example               # Configuration template
pytest.ini                 # Pytest configuration
README.md                  # This file

```

## Configuration

Edit `.env`:

```
OPENAI_API_KEY=your-key
LLM_MODEL=gpt-3.5-turbo
TTS_MODEL=tts-1
TTS_VOICE=alloy
REQUEST_TIMEOUT=30
```

## Endpoints

- `GET /` - Service info and configuration
- `GET /health` - Health check (for monitoring)
- `WebSocket /ws` - Main chat endpoint

## Testing

### Run All Tests

```bash
pytest tests/
```

### Run with Verbose Output

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_models.py       # Test data validation
pytest tests/test_websocket.py    # Test WebSocket endpoints
pytest tests/test_llm_service.py  # Test LLM API integration
pytest tests/test_tts_service.py  # Test TTS API integration
```

### Expected Output

```
tests/test_llm.py .....                    [ 25%]
tests/test_models.py ......                [ 55%]
tests/test_tts.py .....                    [ 80%]
tests/test_websocket.py ....               [100%]

=========== 20 passed in 1.23s ===========
```

### What's Tested

- **test_models.py:** Data validation, input constraints (6 tests)
- **test_websocket.py:** Server endpoints, WebSocket connection (4 tests)
- **test_llm_service.py**: LLM API integration, error handling, timeouts (5 tests)
- **test_tts_service.py**: TTS API integration, audio generation, error handling (5 tests)



All tests verify core functionality, API integration, and comprehensive error handling.


## Troubleshooting

| Issue | Fix |
|-------|-----|
| Connection refused | Server not running: `python -m src.main` |
| Invalid API key | Check `.env` file has correct OPENAI_API_KEY |
| Audio doesn't play | Refresh browser, check browser console |
| Ctrl+C doesn't work | Press Ctrl+C again or use Task Manager |

## Current Limitations

- **Single-user only:** System designed for one connection at a time
- **No persistence:** Messages are lost when server restarts (in-memory only)
- **No authentication:** Anyone with access to URL can connect
- **No audio controls:** Cannot pause, resume, or adjust volume
- **Localhost only:** Not suitable for production without additional security

## Future Improvements & Suggestions

### Short-term (Easy)
- Add multi-user support by tracking per-connection message histories
- Implement SQLite database for message persistence
- Add UI controls for audio playback (pause, stop, replay)
- Display message timestamps and connection status indicators

### Medium-term (Moderate)
- Add user authentication with API keys or JWT tokens
- Implement rate limiting to prevent abuse
- Add message history export (JSON/PDF)
- Support multiple voice options in UI
- Add error recovery and automatic reconnection

### Long-term (Advanced)
- Implement streaming responses for faster feedback
- Add multi-modal support (image input/output)
- Deploy to cloud (AWS, GCP, Azure)
- Add conversation memory and context management
- Implement advanced UI with chat history sidebar

## Tech Stack

- **Backend:** Python, FastAPI, async/await, WebSocket
- **Frontend:** Vanilla JavaScript, WebSocket
- **APIs:** OpenAI Chat Completions, OpenAI Text-to-Speech
- **Server:** Uvicorn, Pydantic

## Open for Suggestions and PRs

Please feel free to raise any PRs and any suggestions
