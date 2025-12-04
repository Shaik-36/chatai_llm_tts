"""
Text to Speech (TTS) Service - Calls OpenAI Text-to-Speech Endpoint
"""

import httpx
from src.config import settings

# ================================================================
#  Text to Speech Service - Sends LLM Text and receive Audio
# ================================================================

async def get_tts_audio(text: str) -> bytes:

    #================ Build Parameters to send to TTS Endpoint ==================
    # API DOCs : https://platform.openai.com/docs/api-reference/audio/createSpeech
    
    url = "https://api.openai.com/v1/audio/speech"
    
    payload = {
        "model": settings.tts_model,
        "input": text,
        "voice": settings.tts_voice,
        "response_format": "mp3"
    }
    
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json"
    }
    
    #============  POST Message to TTS Endpoint and return response ==============
    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.content
    
    #=============================  Handle Exceptions ==============================
    except httpx.HTTPStatusError as e:
        raise Exception(f"OpenAI TTS error: {e.response.status_code}")
    except httpx.TimeoutException:
        raise Exception(f"TTS timeout after {settings.request_timeout}s")
    except httpx.ConnectError:
        raise Exception("Cannot connect to OpenAI")
    except Exception as e:
        raise Exception(f"TTS error: {str(e)}")
